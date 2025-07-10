from django.shortcuts import render
from events.models import *
from django.db.models import Max

def index(request):
    events_with_latest_date = Event.objects.annotate(
        latest_date=Max('dates__date')
    ).filter(latest_date__isnull=False).order_by('-latest_date')

    latest =events_with_latest_date.first()
    last_3 = events_with_latest_date[:3]
    return render(request,"website/index.html",{"latest":latest,"last_3":last_3})

def contact(request):
    return render(request, "website/contact.html",{})

def event_details(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request,"website/event_details.html",{"event": event})

def events(request):
    events_with_latest_date = Event.objects.annotate(
        latest_date=Max('dates__date')
    ).filter(latest_date__isnull=False).order_by('-latest_date')


    return render(request, "website/events.html", {"events": events_with_latest_date})

def aboutus(request):
    return render(request,"website/aboutus.html",{})
