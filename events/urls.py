#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path
from events.views import *

urlpatterns = [
    path("forestallningar", plays_over_time, name="plays_over_time"),
]
