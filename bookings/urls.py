#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path
from bookings.views import *

urlpatterns = [
    path("create/",create),
    path("verify/<uuid:booking_id>/", verify, name="verify-booking"),
]
