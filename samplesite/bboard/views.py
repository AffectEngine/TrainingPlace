from django.shortcuts import render
from django.http import HttpResponse
from bboard.models import FirstModel


def home(request):
    return HttpResponse('<h1>Hello world</h1>')

def inde(request):
    bbs = FirstModel.objects.order_by('-published')
    return render(request, 'bboard/index.html', {'bbs': bbs})