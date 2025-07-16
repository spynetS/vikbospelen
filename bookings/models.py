from django.db import models
import uuid
from django.urls import reverse
from django.template.loader import render_to_string
from events.models import Event, EventDate
from mail.mail import sendmail

class Booking(models.Model):
    name = models.CharField("Namn",max_length=100)
    email = models.EmailField()
    phone = models.CharField("Telefon",max_length=20, blank=True)

    adult_seats = models.PositiveIntegerField("Vuxen platser",default=0)
    child_seats = models.PositiveIntegerField("Barn platser",default=0)

    booking_number = models.UUIDField("Boknings nummer",default=uuid.uuid4, editable=False, unique=True)

    booking_date = models.ForeignKey(EventDate,on_delete=models.CASCADE,related_name="bookings")

    created_at = models.DateTimeField(auto_now_add=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    verified = models.BooleanField("Verifierad",default=False)

    def get_price(self):
        return self.event.price*self.adult_seats

    class Meta:
        verbose_name = "Bokning"
        verbose_name_plural = "Bokningar"

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.name}"

    def send_mail(self,request):
        try:
            relative_url = reverse("booking_verify", args=[self.booking_number])
            verification_link = request.build_absolute_uri(relative_url)

            context = {
                "name": self.name,
                "event": self.event,
                "booking": self,
                "verification_link": verification_link,
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
