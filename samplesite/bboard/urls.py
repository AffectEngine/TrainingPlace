from django.urls import path
from .views import inde, by_rubric, FirstModelCreateView, PersonView

app_name = 'bboard'

urlpatterns = [
    path('add/', FirstModelCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', inde, name='inde'),
    path('users/<int:id>/<str:name>/', PersonView.as_view(), name='bboard'),
]