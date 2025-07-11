from django.contrib import admin
from events.models import Event, EventDate, EventMedia
from bookings.models import Booking

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0  # No extra empty forms
    readonly_fields = ('booking_number', 'verified')
    can_delete = False
    show_change_link = True  # Make booking clickable

class EventDateInline(admin.TabularInline):
    model = EventDate
    extra = 1
    fields = ['datetime']
    ordering = ['datetime']


class EventMediaInline(admin.TabularInline):
    model = EventMedia
    extra = 1
    fields = ['media_type', 'file', 'caption']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price', 'first_datetime_display','get_seats_left','published']
    list_editable = ['published']
    inlines = [EventDateInline, EventMediaInline, BookingInline]

    def first_datetime_display(self, obj):
        first = obj.first_date()
        return first.datetime.strftime('%Y-%m-%d %H:%M') if first else "-"
    first_datetime_display.short_description = "Första datum & tid"

    def get_seats_left(self, obj):
        return obj.get_seats_left()
    get_seats_left.short_description = 'Lediga platser'
