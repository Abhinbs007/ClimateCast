import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timezone

# Replace with your actual API key
API_KEY = "2567f2a1cf4dec48d3e9a0fcf0457e37"

def weather_data_view(request):
    # Check if 'location' and 'date' are in GET parameters
    location = request.GET.get("location", None)
    date = request.GET.get("date", None)  # Date in YYYY-MM-DD format

    if not location:
        return render(request, "weather_data.html", {"error": "Please enter a location to search for weather data."})

    if not date:
        return render(request, "weather_data.html", {"error": "Please enter a valid date in YYYY-MM-DD format."})

    try:
        # Convert the provided date to a UNIX timestamp
        dt_obj = datetime.strptime(date, "%Y-%m-%d")
        dt = int(dt_obj.replace(tzinfo=timezone.utc).timestamp())

        # API endpoint and parameters for location search
        geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        geocoding_params = {
            "q": location,
            "limit": 1,
            "appid": API_KEY,
        }

        # Get latitude and longitude for the location
        geocoding_response = requests.get(geocoding_url, params=geocoding_params)
        geocoding_response.raise_for_status()
        geocoding_data = geocoding_response.json()
        if not geocoding_data:
            return render(request, "weather_data.html", {"error": "Location not found."})

        lat = geocoding_data[0]["lat"]
        lon = geocoding_data[0]["lon"]

        # Prepare for weather data retrieval
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "appid": API_KEY,
        }

        # Get weather data
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Convert temperatures from Kelvin to Celsius
        for item in weather_data.get('data', []):
            item['temp'] = round(item['temp'] - 273.15, 2)
            item['feels_like'] = round(item['feels_like'] - 273.15, 2)

    except ValueError:
        return render(request, "weather_data.html", {"error": "Invalid date format. Please use YYYY-MM-DD."})
    except requests.RequestException as e:
        return render(request, "weather_data.html", {"error": str(e)})

    # Pass the data to the template
    return render(request, "weather_data.html", {"weather_data": weather_data})
