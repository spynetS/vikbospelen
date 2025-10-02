from django.db import models

# Create your models here.
class ContactUser(models.Model):
    title = models.CharField("Titel")
    name  = models.CharField("Namn")
    phone = models.CharField("Telefon", blank=True)
    email = models.CharField("Email", blank=True)

    image = models.ImageField("Profilbild", blank=True)

    published = models.BooleanField("Publicerad",default=True)

    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakter"

    def __str__(self):
        return f"{self.name}"
