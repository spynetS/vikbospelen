from django.shortcuts import render
from events.models import *
from bookings.models import *
from django.db.models import Min, Sum, Max
from django.utils import timezone


def index(request):
    now = timezone.now()

    # Events with at least one future date
    events_with_next_date = Event.objects.filter(
        dates__datetime__gte=now,
        published=True
    ).annotate(
        next_date=Min('dates__datetime')
    ).order_by('next_date')

    next_event = events_with_next_date.first()
    upcoming_3 = events_with_next_date[:3]

    # Fallback if no future events: use latest event based on past dates
    if not next_event:
        fallback_event = Event.objects.filter(
            published=True,
            dates__datetime__lt=now
        ).annotate(
            last_date=Max('dates__datetime')
        ).order_by('-last_date').first()

        next_event = fallback_event

    return render(request, "website/index.html", {
        "latest": next_event,
        "last_3": upcoming_3,
        "now": now
    })


def contact(request):
    return render(request, "website/contact.html",{})

from django.utils import timezone

def event_details(request, slug):
    event = Event.objects.get(slug=slug)

    now = timezone.now()
    today = now.date()

    # Include dates from today onwards
    future_dates = event.dates.filter(datetime__date__gte=today).order_by("datetime")

    dates_with_seats = []
    for date_obj in future_dates:
        seats_left = event.get_seats_left(date_obj)
        dates_with_seats.append({
            'date': date_obj,
            'seats_left': seats_left,
        })

    return render(request, "website/event_details.html", {
        "event": event,
        "dates_with_seats": dates_with_seats,
    })




def events(request):
    events_with_latest_date = Event.objects.annotate(
        latest_date=Max('dates__datetime')
    ).filter(latest_date__isnull=False).order_by('-latest_date')


    return render(request, "website/events.html", {"events": events_with_latest_date})

def aboutus(request):
    return render(request,"website/aboutus.html",{})
