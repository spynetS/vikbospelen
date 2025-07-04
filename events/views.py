from django.shortcuts import render

from django.shortcuts import render
from .models import Event
from django.db.models.functions import ExtractYear
from django.db.models import Count

def plays_over_time(request):
    year = request.GET.get("year")
    if year:
        events = Event.objects.filter(dates__date__year=year).distinct()
    else:
        events = Event.objects.all()

    # Get all years with at least one event
    years_with_events = (
        Event.objects
        .annotate(year=ExtractYear("dates__date"))
        .values("year")
        .annotate(count=Count("id"))
        .order_by("year")
        .values_list("year", flat=True)
    )

    context = {
        "events": events,
        "years_with_events": years_with_events,
    }

    if request.headers.get("HX-Request"):
        return render(request, "components/event_list.html", context)

    return render(request, "website/slider_page.html", context)
