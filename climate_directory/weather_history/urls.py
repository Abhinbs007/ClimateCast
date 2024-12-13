from django.urls import path
from . import views
urlpatterns = [
    path("index.html", views.weather_history_view, name="weather_history_view"),

]