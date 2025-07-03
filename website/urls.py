#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path
from website.views import *

urlpatterns = [
    path('forestallningar', events),
    path('forestallningar/<slug:slug>', index, name="event_detail"),
]
