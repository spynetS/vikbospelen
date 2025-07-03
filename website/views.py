from django.shortcuts import render
from events.models import *

def index(request):
    latest = Event.objects.order_by('-id').first()
    return render(request,"website/index.html",{"latest":latest})

def event_details(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request,"website/event_details.html",{"event": event})

def events(request):
    return render(request,"website/events.html",{"events": Event.objects.all()})
