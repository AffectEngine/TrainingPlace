from django.shortcuts import render
from django.http import HttpResponse
from dokk.models import SecondModel


def indek(request):
    bekk = SecondModel.objects.order_by('-published')
    return render(request, 'dokk/indek.html', {'bekk':bekk})

