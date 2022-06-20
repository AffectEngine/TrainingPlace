from django.shortcuts import render
from django.http import HttpResponse
from models import FirstModel

def home(request):
    return HttpResponse('<h1>Hello world</h1>')

def inde(request):
    s = 'Список объявлений\r\n\r\n\r\n'
    for spob in FirstModel.objects.order_by('-published'):
        s += spob.title + '\r\n' + spob.content + '\r\n\r\n'
    return HttpResponse(s, content_type='text/plain; charset=utf-8')
