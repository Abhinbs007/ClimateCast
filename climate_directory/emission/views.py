from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import requests

def get_emissions_sources(request):
    if request.method == 'POST':
        limit = request.POST.get('limit', 100)
        year = request.POST.get('year')
        offset = request.POST.get('offset', 0)
        countries = request.POST.get('countries', '').split(',')
        sectors = request.POST.get('sectors', '').split(',')

        # Updated API URL
        url = "https://api.climatetrace.org/v6/assets"
        params = {
            "limit": limit,
            "offset": offset
        }

        if year:
            params["year"] = year
        if countries:
            params["countries"] = ','.join(countries)
        if sectors:
            params["sectors"] = ','.join(sectors)

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": response.status_code, "message": response.text}, status=response.status_code)

    return render(request, 'emission_form.html')
