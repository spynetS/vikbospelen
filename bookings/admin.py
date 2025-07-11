from django.contrib import admin
from bookings.models import Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'adult_seats', 'child_seats', 'booking_number', 'verified')
    list_filter = ('verified', 'event')
    search_fields = ('name', 'email', 'booking_number')
