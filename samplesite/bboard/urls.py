from django.urls import path
from .views import inde, by_rubric, FirstModelCreateView, PersonView


urlpatterns = [
    path('add/', FirstModelCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', inde, name='inde'),
    path('ppl/', PersonView.as_view(), name='ppl'),
]