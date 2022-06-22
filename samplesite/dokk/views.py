from django.shortcuts import render
from django.http import HttpResponse
from dokk.models import SecondModel


def indek(request):
    bekk = SecondModel.objects.all()

