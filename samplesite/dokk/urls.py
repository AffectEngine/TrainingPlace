from django.urls import path
from dokk.views import indek
from django.contrib import admin

urlpatterns = [
    path('', indek),
]
