from bboard.models import FirstModel, Rubric
from .forms import FirstModelForm, PersonForm

from django.template.loader import get_template
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, FileResponse

# from django.views.generic.base import TemplateView   Попытка замены TemplateView на ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView, ArchiveIndexView


def home(request):
    home_image = open('bboard/images_site/cat_kambare.png', 'rb')
    return FileResponse(home_image)


def inde(request):
    firstmodelsource = FirstModel.objects.all()
    rubrics = Rubric.objects.all()
    context = {'firstmodelsource': firstmodelsource, 'rubrics': rubrics}
    template = get_template('bboard/index.html')
    return HttpResponse(template.render(context=context, request=request))


# ОБЫЧНЫЙ КОНТРОЛЛЕР ВЫВОДА РУБРИК ПО ИХ КЛЮЧУ (ЗАМЕНЕНО к-к FirstModelByRubricView)

# def by_rubric(request, rubric_id):
#     firstmodelsource = FirstModel.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'firstmodelsource': firstmodelsource, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'bboard/by_rubric.html', context)


# ПЛОХАЯ ПРАКТИКА МАССОВОГО КОММЕНТАРИЯ, замена обычной формы создания Нового Объявления на FormView к-к

# def create_and_save(request):
#     if request.method == 'POST':
#         cre_a_sav_form = FirstModelForm(request.POST)
#         if cre_a_sav_form.is_valid():
#             cre_a_sav_form.save()
#             return HttpResponseRedirect(
#                 reverse('bboard:by_rubric', kwargs={'rubric_id': cre_a_sav_form.cleaned_data['rubric'].pk}))
#         else:
#             context = {'form': cre_a_sav_form}
#             return render(request, 'bboard/create.html', context)
#     else:
#         cre_a_sav_form = FirstModelForm()
#         context = {'form': cre_a_sav_form}
#         return render(request, 'bboard/create.html', context)

# ПЛОХАЯ ПРАКТИКА МАССОВОГО КОММЕНТАРИЯ, замена обычной формы создания Нового Объявления на FormView к-к

# class FirstModelCreateView(CreateView):
#     template_name = 'bboard/create.html'
#     model = FirstModel
#     form_class = FirstModelForm
#     success_url = reverse_lazy('bboard:inde')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context


class FirstModelEditView(UpdateView):
    template_name = 'bboard/firstmodel_form.html'
    model = FirstModel
    form_class = FirstModelForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super(FirstModelEditView, self).get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class FirstModelDeleteView(DeleteView):
    template_name = 'bboard/firstmodel_confirm_delete.html'
    model = FirstModel
    success_url = reverse_lazy('bboard:inde')
    queryset = FirstModel.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(FirstModelDeleteView, self).get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class FirstModelAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = FirstModelForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super(FirstModelAddView, self).get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super(FirstModelAddView, self).get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class PersonView(CreateView):
    template_name = 'bboard/people.html'
    form_class = PersonForm
    success_url = '/bboard/'

    def get_absolute_url(self):
        return f'/person/{self.pk}/'


# BAD PRACTICE массовый комментарий с попыткой замены TemplateView на ListView для пробы пера

# class FirstModelByRubricView(TemplateView):
#
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(FirstModelByRubricView, self).get_context_data(**kwargs)
#         context['firstmodelsource'] = FirstModel.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


class FirstModelByRubricViewL(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'firstmodelsource'

    def get_queryset(self):
        return FirstModel.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(FirstModelByRubricViewL, self).get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])

        return context


class FirstModelDetailView(DetailView):
    model = FirstModel

    def get_context_data(self, **kwargs):
        context = super(FirstModelDetailView, self).get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class FirstModelIndexView(ArchiveIndexView):
    model = FirstModel
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'firstmodelsource'
    allow_empty = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class FirstModelArchiveView(YearArchiveView):
    queryset = Rubric.objects.all()
    date_field = 'published'
    template_name = 'bboard/index.html'
    context_object_name = 'firstmodelsource'
    year = '2022'
    allow_empty = True
    allow_future = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
