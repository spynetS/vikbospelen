from django.contrib import admin
from events.models import Event, EventDate, EventMedia
from bookings.models import Booking
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Event
from bookings.models import Booking
from django import forms
import csv
from datetime import datetime

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0  # No extra empty forms
    readonly_fields = ('booking_number', 'verified')
    can_delete = False
    show_change_link = True  # Make booking clickable

    
class EventDateInlineForm(forms.ModelForm):
    year = forms.IntegerField(
        label="År",
        required=False,
        min_value=1900,
        max_value=2100
    )

    class Meta:
        model = EventDate
        fields = ("year_only", "datetime", "year")

    def clean(self):
        cleaned = super().clean()
        year_only = cleaned.get("year_only")
        year = cleaned.get("year")
        dt = cleaned.get("datetime")

        if year_only:
            if not year:
                raise forms.ValidationError("Ange ett år")
            cleaned["datetime"] = datetime(year, 1, 1)
        else:
            if not dt:
                raise forms.ValidationError("Ange datum och tid")

        return cleaned

class EventDateInline(admin.TabularInline):
    model = EventDate
    form = EventDateInlineForm
    extra = 1
    fields = ("year_only", "datetime", "year")
    ordering = ("datetime",)

    class Media:
        js = ("admin/js/eventdate_inline.js",)
        
class EventMediaInline(admin.TabularInline):
    model = EventMedia
    extra = 1
    fields = ['media_type', 'file', 'caption']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price', 'first_datetime_display','published']
    list_editable = ['published']
    inlines = [EventDateInline, EventMediaInline, BookingInline]
    actions = ["view_booking_overview"]


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:event_id>/booking-overview/', self.admin_site.admin_view(self.booking_overview), name="booking-overview"),
            path('<int:event_id>/booking-csv/', self.admin_site.admin_view(self.booking_overview_csv), name="booking-overview-csv"),
        ]
        return custom_urls + urls

    def view_booking_overview(self, request, queryset):
        if queryset.count() == 1:
            event = queryset.first()
            return HttpResponse(
                f'<script>window.location.href="/admin/events/event/{event.id}/booking-overview/";</script>'
            )
        else:
            self.message_user(request, "Please select a single event to view its booking overview.")

    view_booking_overview.short_description = "View booking overview"

    def booking_overview(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        bookings = event.bookings.select_related("booking_date").all()

        context = {
            "event": event,
            "bookings": bookings,
            "title": f"Booking Overview for {event.title}",
        }

        return render(request, "admin/booking_overview.html", context)

    def booking_overview_csv(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        bookings = event.bookings.filter(verified=True).select_related("booking_date").all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Bokningar__{event.title}.csv"'

        writer = csv.writer(response)
        #writer.writerow(['Name', 'Email', 'Phone', 'Adult Seats', 'Child Seats', 'Total Seats', 'Date & Time','Cost'])
        writer.writerow(['Namn', 'Email', 'Telefon', 'Platser', 'Datum och tid','Att betala'])

        for booking in bookings:
            writer.writerow([
                booking.name,
                booking.email,
                booking.phone,
                booking.adult_seats,
                #booking.child_seats,
                #booking.adult_seats + booking.child_seats,
                booking.booking_date.datetime.strftime('%Y-%m-%d %H:%M'),
                str(event.price*(booking.adult_seats+booking.child_seats))+"kr"
            ])

        return response

    def first_datetime_display(self, obj):
        first = obj.first_date()
        return first.datetime.strftime('%Y-%m-%d %H:%M') if first else "-"
    first_datetime_display.short_description = "Första datum & tid"

