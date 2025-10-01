from django.shortcuts import render
from .models import Event
from django.db.models import Max, Q, Count
from django.db.models.functions import ExtractYear
from django.utils import timezone

def plays_over_time(request):
    year = request.GET.get("year")
    search = request.GET.get("search", "").strip()

    now = timezone.now()

    # Only include events that have at least one date in the past or now
    events = Event.objects.annotate(
        latest_date=Max('dates__datetime')
    ).filter(
        latest_date__isnull=False,
        latest_date__lte=now
    )

    if year:
        try:
            events = events.filter(dates__datetime__year=int(year))
        except ValueError:
            pass

    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    events = events.distinct()

    years_with_events = (
        Event.objects
        .annotate(year=ExtractYear("dates__datetime"))
        .values("year")
        .annotate(count=Count("id", distinct=True))
        .order_by("year")
        .values_list("year", flat=True)
    )

    context = {
        "events": events,
        "years_with_events": years_with_events,
        "search": search,
        "selected_year": year,
    }

    if request.headers.get("HX-Request"):
        return render(request, "components/event_list.html", context)

    return render(request, "website/slider_page.html", context)
