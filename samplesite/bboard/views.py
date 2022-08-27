from bboard.models import FirstModel, Rubric, Person
from .forms import RegisterPersonForm, FirstModelFullForm

from django.forms import modelformset_factory, inlineformset_factory, BaseModelFormSet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, FileResponse
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.template.loader import get_template
from django.forms.formsets import ORDERING_FIELD_NAME
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# from django.views.generic.base import TemplateView   Попытка замены TemplateView на ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


def home(request):
    home_image = open('D:/pythonProject/samplesite/bboard/static/bboard/img/cat_kambare.png', 'rb')
    return FileResponse(home_image)


@login_required
def inde(request):
    firstmodelsource = FirstModel.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(firstmodelsource, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'firstmodelsource': page.object_list}
    return render(request, 'bboard/index.html', context)


@login_required
def edit(request, pk):
    firstmodel = FirstModel.objects.get(pk=pk)
    if request.method == 'POST':
        firstmodeledit = FirstModelFullForm(request.POST, instance=firstmodel)
        if firstmodeledit.is_valid():
            if firstmodeledit.has_changed():
                firstmodeledit.save()
                return HttpResponseRedirect(
                    reverse('bboard:by_rubric', kwargs={'rubric_id': firstmodeledit.cleaned_data['rubric'].pk})
                )
            else:
                return HttpResponseRedirect(
                    reverse('bboard:by_rubric', kwargs={'rubric_id': firstmodeledit.cleaned_data['rubric'].pk})
                )
        else:
            context = {'form': firstmodeledit}
            return render(request, 'bboard/firstmodel_edit_form.html', context)
    else:
        firstmodeledit = FirstModelFullForm(instance=firstmodel)
        context = {'form': firstmodeledit}
        return render(request, 'bboard/firstmodel_edit_form.html', context)


@login_required
@permission_required(('bboard.delete_rubric'), raise_exception=True)
def delete(request, pk):
    firstmodel = FirstModel.objects.get(pk=pk)
    if request.method == 'POST':
        firstmodel.delete()
        return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': firstmodel.rubric.pk}))
    else:
        context = {'firstmodel': firstmodel}
        return render(request, 'bboard/firstmodel_confirm_delete.html', context)


def contact(request):
    return HttpResponse('Контактный вид')


class FirstModelRedirectView(RedirectView):
    url = 'https://www.youtube.com/watch?v=nuKIatYN50U&ab_channel=JAG'


class FirstModelAddView(LoginRequiredMixin, FormView):
    template_name = 'bboard/create.html'
    form = FirstModelFullForm
    form_class = FirstModelFullForm

    def get_context_data(self, *args, **kwargs):
        context = super(FirstModelAddView, self).get_context_data(**kwargs)
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


class FirstModelByRubricViewL(LoginRequiredMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'firstmodelsource'

    def get_queryset(self):
        return FirstModel.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(FirstModelByRubricViewL, self).get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])

        return context


class FirstModelDetailView(LoginRequiredMixin, DetailView):
    model = FirstModel
    form_class = FirstModelFullForm

    def get_context_data(self, **kwargs):
        context = super(FirstModelDetailView, self).get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class PersonRegView(FormView):
    template_name = 'bboard/people.html'
    form_class = RegisterPersonForm

    def get_context_data(self, *args, **kwargs):
        context = super(PersonRegView, self).get_context_data(**kwargs)
        context['name'] = Person.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super(PersonRegView, self).get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:person_display')


class PersonDisplayView(UserPassesTestMixin, ListView):
    template_name = 'bboard/person_display.html'
    context_object_name = 'personmodelsource'
    paginate_by = 3
    permission_denied_message = 'У вас недостаточно прав для доступа к этой странице.'

    def get_queryset(self):
        return Person.objects.all()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(PersonDisplayView, self).get_context_data(**kwargs)
        return context

    def test_func(self):
        return self.request.user.is_staff


class RubricFormSetValidation(BaseModelFormSet):
    def clean(self):
        super(RubricFormSetValidation, self).clean()
        names = [form.cleaned_data['name'] for form in self.forms if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names) or ('Мебель' not in names) or (
                'Завод' not in names) or ('Кладбище' not in names):
            raise ValidationError('Добавьте рубрики недвижимости, транспорта, мебели, завода и кладбища')


@login_required
def rubrics(request):
    RubricFormSet = modelformset_factory(
        Rubric, fields=('name',), can_order=True, can_delete=True, extra=2, formset=RubricFormSetValidation
    )

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save()
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()
            return redirect('bboard:rubrics')
    else:
        formset = RubricFormSet(
            initial=[{'name': 'Новая рубрика'}, {'name': 'Ещё одна новая рубрика'}], queryset=Rubric.objects.all()[0:5]
        )
    context = {'formset': formset}
    return render(request, 'bboard/rubric.html', context)


@login_required
def first_model_inline_formset(request, rubric_id):
    FirstModelInlineFormSet = inlineformset_factory(Rubric, FirstModel, form=FirstModelFullForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = FirstModelInlineFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('bboard:rubrics')
    else:
        formset = FirstModelInlineFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/rubricsID.html', context)

# def inde(request):
#     firstmodelsource = FirstModel.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'firstmodelsource': firstmodelsource, 'rubrics': rubrics}
#     template = get_template('bboard/index.html')
#     return HttpResponse(template.render(context=context, request=request))


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

# ПЛОХАЯ ПРАКТИКА МАССОВОГО КОММЕНТАРИЯ, замена UpdateView на К-Ф edit для правки записи по pk из URL

# class FirstModelEditView(UpdateView):
#     template_name = 'bboard/firstmodel_edit_form.html'
#     model = FirstModel
#     form_class = FirstModelForm
#     success_url = '/'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(FirstModelEditView, self).get_context_data(*args, **kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context

# ПЛОХАЯ ПРАКТИКА МАССОВОГО КОММЕНТАРИЯ, замена DeleteView на К-Ф delete для удаления записи по pk из URL

# class FirstModelDeleteView(DeleteView):
#     template_name = 'bboard/firstmodel_confirm_delete.html'
#     model = FirstModel
#     success_url = reverse_lazy('bboard:inde')
#     queryset = FirstModel.objects.all()
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(FirstModelDeleteView, self).get_context_data(*args, **kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context

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
