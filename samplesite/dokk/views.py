from django.shortcuts import render
from django.http import HttpResponse
from dokk.models import SecondModel


def indek(request):
    return HttpResponse('<h1>Hello world2</h1>')

