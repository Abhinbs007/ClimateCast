from django.urls import path
from . import views

urlpatterns = [
    path('get_disaster_data.html', views.get_disaster_data, name='get_disaster_data'),
]
