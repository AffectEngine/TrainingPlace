from django.urls import path
from .views import inde, PersonView, FirstModelByRubricViewL, FirstModelDetailView, FirstModelAddView, FirstModelEditView, FirstModelDeleteView

app_name = 'bboard'

urlpatterns = [
    path('add/', FirstModelAddView.as_view(), name='add'),
#    path('<int:rubric_id>/', by_rubric, name='by_rubric'), (ОБЫЧНЫЙ ПУТЬ ВЫВОДА РУБРИК ПО ИХ КЛЮЧУ (ЗАМЕНЕНО as_view FirstModelByRubricView)
    path('', inde, name='inde'),
    path('users/<int:id>/<str:name>/', PersonView.as_view(), name='bboard'),
#    path('<int:rubric_id>/', FirstModelByRubricView.as_view(), name='by_rubric'), (Замены урла TemplateView на ListView)
    path('<int:rubric_id>/', FirstModelByRubricViewL.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', FirstModelDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', FirstModelEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', FirstModelDeleteView.as_view(), name='rub-delete')
]