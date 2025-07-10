from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Event(models.Model):
    title = models.CharField("Titel", max_length=255)
    poster = models.ImageField("Affisch", upload_to='event_posters/')
    short_description = models.CharField("Kort beskrivning", max_length=300)
    description = models.TextField("Beskrivning")
    price = models.DecimalField("Pris", max_digits=10, decimal_places=2)
    location = models.CharField("Plats", max_length=255)
    slug = models.SlugField("Slug",unique=True, blank=True, help_text="sökväg i webbläsaren (kan lämnas tom)")
    published = models.BooleanField(
        "Publicerad",
        default=True,
        help_text="Markera om objektet ska vara publicerat"
    )
    def first_date(self):
        return self.dates.order_by("datetime").first()

    def __str__(self):
        return self.title or "No Title"


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
    event = models.ForeignKey(Event, verbose_name="Evenemang", on_delete=models.CASCADE, related_name='dates')
    datetime = models.DateTimeField("Datum och tid")

    class Meta:
        verbose_name = "Datum"
        verbose_name_plural = "Datum"

    def __str__(self):
        datetime_str = self.datetime.strftime('%Y-%m-%d %H:%M') if self.datetime else "No date"
        title_str = self.event.title if self.event and self.event.title else "No title"
        return f"{datetime_str} för {title_str}"

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
