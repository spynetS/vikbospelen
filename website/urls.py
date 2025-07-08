#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path
from website.views import *

urlpatterns = [
    path("",index),
    path('kontakt', contact,name="contact"),
    path('forestallningar/<slug:slug>', event_details, name="event_detail"),
]
