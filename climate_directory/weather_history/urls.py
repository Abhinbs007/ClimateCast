from django.urls import path
from . import views

urlpatterns = [
    path('weather_data.html', views.weather_data_view, name='weather_data_view'),
]
