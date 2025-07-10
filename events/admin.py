from django.contrib import admin
from events.models import Event, EventDate, EventMedia


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
    list_display = ['title', 'location', 'price', 'first_datetime_display']
    inlines = [EventDateInline, EventMediaInline]

    def first_datetime_display(self, obj):
        first = obj.first_date()
        return first.datetime.strftime('%Y-%m-%d %H:%M') if first else "-"
    first_datetime_display.short_description = "Första datum & tid"
