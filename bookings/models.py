from django.db import models
import uuid

from django.template.loader import render_to_string
from events.models import Event
from mail.mail import sendmail

class Booking(models.Model):
    name = models.CharField("Namn",max_length=100)
    email = models.EmailField()
    phone = models.CharField("Telefon",max_length=20, blank=True)

    adult_seats = models.PositiveIntegerField("Vuxen platser",default=0)
    child_seats = models.PositiveIntegerField("Barn platser",default=0)

    booking_number = models.UUIDField("Boknings nummer",default=uuid.uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    verified = models.BooleanField("Verifierad",default=False)

    class Meta:
        verbose_name = "Bokning"
        verbose_name_plural = "Bokningar"

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.name}"

    def send_mail(self):
        try:
            context= {
                "name": self.name,
                "event": self.event,
                "booking": self,
                "verification_link": f"http://localhost:8000/bookings/verify/{self.booking_number}",
                "theater_name": "Vikbolandsspelet",
            }

            html_content = render_to_string("emails/booking_verification.html", context)

            sendmail(
                "Bokings verifiering",
                html_content,
                self.name,
                "",
                self.email,
                None,
                "html"
            )
            return True
        except:
            return False
