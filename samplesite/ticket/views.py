from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View, TemplateView


class MyView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Django Classes')


class MyTempView(TemplateView):

    template_name = "ticket/add-ticket.html"

    def get_context_data(self, **kwargs):
        context = super(MyTempView, self).get_context_data(**kwargs)
        context["text"] = "Flash in the Night"
        return context

