from django.urls import path
from .views import inde, by_rubric


urlpatterns = [
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', inde, name='inde'),
]