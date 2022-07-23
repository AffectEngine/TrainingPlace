from django.urls import path
from .views import inde, FirstModelCreateView, PersonView, FirstModelByRubricView, FirstModelDetailView

app_name = 'bboard'

urlpatterns = [
    path('add/', FirstModelCreateView.as_view(), name='add'),
#    path('<int:rubric_id>/', by_rubric, name='by_rubric'), (ОБЫЧНЫЙ ПУТЬ ВЫВОДА РУБРИК ПО ИХ КЛЮЧУ (ЗАМЕНЕНО as_view FirstModelByRubricView)
    path('', inde, name='inde'),
    path('users/<int:id>/<str:name>/', PersonView.as_view(), name='bboard'),
    path('<int:rubric_id>/', FirstModelByRubricView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', FirstModelDetailView.as_view(), name='detail'),
]