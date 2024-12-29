from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_data_view, name='weather_data_view'),
]
