from django.urls import path
from .views import inde

urlpatterns = [
    path('', inde),
]