from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from events.models import Event, EventDate
from bookings.models import Booking
from django.db.models import Sum
# Create your views here.
def verify(request, booking_id):

    booking = get_object_or_404(Booking, booking_number=booking_id)

    if booking.verified:
        return render(request,"website/verified.html", {"msg":"Denna bokning är redan verifierad."})


    booking.verified = True
    booking.save()

    return render(request,"website/verified.html", {"msg":"Tack! Din bokning är verifierad"})

def create(request):
    try:
        event: Event = Event.objects.get(pk=request.POST['event_id'])

        if request.POST['name'] == "" or request.POST['email'] == "" or request.POST['phone'] == "" or request.POST['event_date'] == "Välj Datum" or request.POST['event_date'] == "":
            raise ValueError("Måste fylla i alla fält")

        adult_seats_raw = request.POST["adult_seats"]
        child_seats_raw = request.POST["child_seats"]

        # Convert to int or fallback to 0
        adult_seats = int(adult_seats_raw) if adult_seats_raw.isdigit() else 0
        child_seats = int(child_seats_raw) if child_seats_raw.isdigit() else 0

        booking_date = EventDate.objects.get(pk=request.POST['event_date'])

        # Optional check to ensure at least one seat is booked
        if adult_seats + child_seats == 0:
            raise ValueError("Du måste boka minst 1 plats.")


        if (event.get_number_of_booked_seats(booking_date) + (adult_seats + child_seats)) > event.seats:
            raise ValueError("Finns inte tillräckligt med platser")

        
        booking: Booking = Booking(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            booking_date=booking_date,
            adult_seats = adult_seats,
            child_seats = child_seats,
            event=event
        )
        booking.save()
        if not booking.send_mail(request):
            raise ValueError("Kunde inte skicka mail")

        return render(request,"components/Alert.html",{"type":"sucess","msg":"Bokings mail skickat. Kolla din mail för att verifiera bokningen!"})
    except Exception as e:
        return render(request,"components/Alert.html",{"type":"error","msg":f"Något gick fel: ({e})"})
