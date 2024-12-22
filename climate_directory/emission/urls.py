from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('emission_form.html', views.get_emissions_sources, name='get_emissions_sources'),
    path('country_code.html',views.countrycode,name='get_country_code')
]
