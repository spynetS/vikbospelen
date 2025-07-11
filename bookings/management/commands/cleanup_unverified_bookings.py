#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking

class Command(BaseCommand):
    help = 'Deletes unverified bookings older than 24 hours'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timedelta(hours=0.17)
        deleted, _ = Booking.objects.filter(verified=False, created_at__lt=expiration_time).delete()
        self.stdout.write(f'Deleted {deleted} unverified bookings')
