from django.urls import path
from internet.views import calculate_performance

urlpatterns = [
    path('calculate/', calculate_performance, name='calculate_performance'),
]