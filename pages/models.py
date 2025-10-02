from django.db import models

# Create your models here.
class Page(models.Model):
    url = models.CharField("Url till sidan")
    main_text = models.TextField("Övertext")

    class Meta:
        verbose_name = "Sida"
        verbose_name_plural = "Sidor"

    def __str__(self):
        return f"{self.url}"
