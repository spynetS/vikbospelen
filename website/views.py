from django.shortcuts import render
from events.models import *

# Create your views here.
def index(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request,"website/event_details.html",{"event": event})

def events(request):
    return render(request,"website/events.html",{"events": Event.objects.all()})
