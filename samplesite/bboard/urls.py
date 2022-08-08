from django.urls import path
from .views import inde, edit, delete, PersonRegView, FirstModelByRubricViewL, FirstModelDetailView, FirstModelAddView, \
    ArchiveIndexView, YearArchiveView, FirstModelDetailDateView, FirstModelRedirectView, \
    RegisterPersonForm, PersonDisplayView

app_name = 'bboard'

urlpatterns = [
    #    path('<int:rubric_id>/', by_rubric, name='by_rubric'), (ОБЫЧНЫЙ ПУТЬ ВЫВОДА РУБРИК ПО ИХ КЛЮЧУ (ЗАМЕНЕНО as_view FirstModelByRubricView),
    #    path('<int:rubric_id>/', FirstModelByRubricView.as_view(), name='by_rubric'), (Замены урла TemplateView на ListView),
    # path('edit/<int:pk>/', FirstModelEditView.as_view(), name='edit'), (Замена UpdateView на к-ф edit для правки записи по pk из URL)
    # path('delete/<int:pk>/', FirstModelDeleteView.as_view(), name='rub-delete'), (Замена DeleteView на к-ф delete для удаления записи по pk из URL)
    path('add/', FirstModelAddView.as_view(), name='add'),
    path('', inde, name='inde'),
    path('people/', PersonRegView.as_view(), name='people'),
    path('personlist/', PersonDisplayView.as_view(), name='person_display'),
    path('<int:rubric_id>/', FirstModelByRubricViewL.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', FirstModelDetailView.as_view(), name='detail'),
    path('bboard/xdd/', FirstModelRedirectView.as_view(), name='detail-redir'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('archive/', ArchiveIndexView.as_view(), name="rub-archive"),
    path('<int:year>/', YearArchiveView.as_view(), name='rub-year-archive'),
    path('detaildate/<int:year>/<int:month>/<int:day>/<int:pk>/', FirstModelDetailDateView.as_view(),
         name='detail-date'),
]
