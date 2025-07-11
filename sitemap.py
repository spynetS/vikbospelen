# sitemap.py

from django.contrib.sitemaps import Sitemap
from events.models import Event
from bookings.models import Booking  # if bookings are public

class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Event.objects.filter(published=True)

    def location(self, obj):
        return obj.get_absolute_url()

# Add more sitemaps if needed...

sitemaps = {
    "events": EventSitemap,
}
