from django.contrib import admin
from events.models import *
# Register your models here.


class EventDateInline(admin.TabularInline):
    model = EventDate
    extra = 1

class EventMediaInline(admin.TabularInline):
    model = EventMedia
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price']
    inlines = [EventDateInline, EventMediaInline]

admin.site.register(EventMedia)
