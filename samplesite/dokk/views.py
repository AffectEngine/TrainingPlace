from django.shortcuts import render
from django.http import HttpResponse
from dokk.models import SecondModel


def hometwo(request):
    return HttpResponse('<h1>Hello world</h1>')

def indek(request):
    bb = SecondModel.objects.order_by('-published')
    return render(request, 'dokk/indek.html', {'bb': bb})