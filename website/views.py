from django.shortcuts import render
from events.models import *
from bookings.models import *
from django.db.models import Min, Sum
from django.utils import timezone

def index(request):
    now = timezone.now()

    # Only include events that have at least one future date
    events_with_next_date = Event.objects.filter(
        dates__datetime__gte=now,
        published=True
    ).annotate(
        next_date=Min('dates__datetime')
    ).order_by('next_date')

    next_event = events_with_next_date.first()
    upcoming_3 = events_with_next_date[:3]

    return render(request, "website/index.html", {
        "latest": next_event,
        "last_3": upcoming_3,
        "now": now
    })

def contact(request):
    return render(request, "website/contact.html",{})

def event_details(request, slug):
    event = Event.objects.get(slug=slug)

    dates_with_seats = []
    for date in event.dates.filter(datetime__gte=timezone.now()).order_by("datetime"):
        seats_left = event.get_seats_left(date)
        dates_with_seats.append({
            'date': date,
            'seats_left': seats_left,
        })

    return render(request,"website/event_details.html",{"event": event, 'dates_with_seats': dates_with_seats})

def events(request):
    events_with_latest_date = Event.objects.annotate(
        latest_date=Max('dates__datetime')
    ).filter(latest_date__isnull=False).order_by('-latest_date')


    return render(request, "website/events.html", {"events": events_with_latest_date})

def aboutus(request):
    return render(request,"website/aboutus.html",{})
