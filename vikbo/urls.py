from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from sitemap import sitemaps  # <-- your root sitemap.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("website.urls")),
    path("",include("events.urls")),
    path("mail/",include("mail.urls")),
    path("bookings/",include("bookings.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
