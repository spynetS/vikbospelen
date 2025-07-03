from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='event_posters/')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.title

class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField()

    def __str__(self):
        return f"{self.date} for {self.event.title}"

class EventMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='event_media/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.media_type.capitalize()} for {self.event.title}"
