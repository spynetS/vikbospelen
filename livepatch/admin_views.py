from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


def dashboard(request):
    return render(request, "livepatch/admin/dashboard.html", {})
