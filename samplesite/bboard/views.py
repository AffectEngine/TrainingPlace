from django.shortcuts import render
from .models import Rubric
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from bboard.models import FirstModel
from django.views.generic.edit import CreateView
from .forms import FirstModelForm, PersonForm
from django.urls import reverse_lazy, reverse
from django.template.loader import get_template


def home(request):
    new_home = HttpResponse('Здесь будет', content_type='text/plain; charset=utf-8')
    new_home.write(' главная')
    new_home.writelines((' страница', ' сайта'))
    new_home['keywords'] = 'Python, Django'
    return new_home


def inde(request):
    bbs = FirstModel.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    template = get_template('bboard/index.html')
    return HttpResponse(template.render(context=context, request=request))


def by_rubric(request, rubric_id):
    bbs = FirstModel.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


def create_and_save(request):
    if request.method == 'POST':
        cre_a_sav_form = FirstModelForm(request.POST)
        if cre_a_sav_form.is_valid():
            cre_a_sav_form.save()
            return HttpResponseRedirect(
                reverse('bboard:by_rubric', kwargs={'rubric_id': cre_a_sav_form.cleaned_data['rubric'].pk}))
        else:
            context = {'form': cre_a_sav_form}
            return render(request, 'bboard/create.html', context)
    else:
        cre_a_sav_form = FirstModelForm()
        context = {'form': cre_a_sav_form}
        return render(request, 'bboard/create.html', context)


class FirstModelCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = FirstModelForm
    success_url = reverse_lazy('bboard:inde')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class PersonView(CreateView):
    template_name = 'bboard/people.html'
    form_class = PersonForm
    success_url = '/bboard/'

    def get_absolute_url(self):
        return f'/person/{self.pk}/'
