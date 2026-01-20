from django.db import models
from django.db.models import Min, Sum
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from datetime import timedelta

class Event(models.Model):
    title = models.CharField("Titel", max_length=255)
    poster = models.ImageField("Affisch", upload_to='event_posters/')
    short_description = models.CharField("Kort beskrivning", max_length=300)
    description = models.TextField("Beskrivning")
    price = models.DecimalField("Pris", max_digits=10, decimal_places=2,blank=True, default=0)
    location = models.CharField("Plats", max_length=255, blank=True, default="")
    slug = models.SlugField("Slug",unique=True, blank=True, help_text="sökväg i webbläsaren (kan lämnas tom)")
    published = models.BooleanField(
        "Publicerad",
        default=True,
        help_text="Markera om objektet ska vara publicerat"
    )

    salver_link = models.CharField("Salver länk (biljätter)", blank=True)

    seats = models.IntegerField("Antal platser per datum",help_text="Detta är totala antalet platser som går att boka på hemsidan", blank=True, default=0)
    can_book = models.BooleanField("Går att boka",blank=True, help_text="Hemsidans innbygda boknings system")

    @property
    def is_past(self):
        """
        Returns True if all EventDates are in the past.
        Returns False if at least one EventDate is in the future or now.
        """
        now = timezone.now()
        return not self.dates.filter(datetime__gte=now).exists()    
    
    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})

    def first_date(self):
        return self.dates.order_by("datetime").first()

    def __str__(self):
        return self.title or "No Title"

    def get_number_of_booked_seats(self, booking_date):
        # This code will retrive bookings for this event and that are either verified
        # or not older then 5minutes and return the total amount of seats
        now = timezone.now()
        five_minutes_ago = now - timedelta(minutes=5)

        booked = self.bookings.filter(
            booking_date=booking_date
        ).filter(
            Q(verified=True) |
            Q(verified=False, created_at__gte=five_minutes_ago)
        ).aggregate(
            total_adults=Sum('adult_seats'),
            total_children=Sum('child_seats')
        )
        return (booked['total_adults'] or 0) + (booked['total_children'] or 0)


    def get_seats_left(self, booking_date):
        return self.seats - self.get_number_of_booked_seats(booking_date)


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Evenemang"
        verbose_name_plural = "Evenemang"

    def get_next_date(self):
        return self.dates.filter(datetime__gte=timezone.now()).order_by('datetime').first()

    
class EventDate(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name="Evenemang",
        on_delete=models.CASCADE,
        related_name="dates"
    )
    datetime = models.DateTimeField("Datum och tid", blank=True, null=True)
    year_only = models.BooleanField("Endast år", default=False)
    
    class Meta:
        verbose_name = "Datum"
        verbose_name_plural = "Datum"

    def __str__(self):
        if self.year_only and self.datetime:
            return str(self.datetime.year)
        return self.datetime.strftime("%Y-%m-%d %H:%M")
    
class EventMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Bild'),
        ('video', 'Video'),
    ]

    event = models.ForeignKey(Event, verbose_name="Evenemang", on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField("Media-typ", max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField("Fil", upload_to='event_media/')
    caption = models.CharField("Bildtext", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medier"

    def __str__(self):
        return f"{self.get_media_type_display()} för {self.event.title}" or "Nope"
