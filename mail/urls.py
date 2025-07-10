#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path
from mail.views import *

urlpatterns = [
    path("contact", contact),
]
