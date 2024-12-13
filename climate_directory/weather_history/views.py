from django.shortcuts import render
import requests
from datetime import datetime

import requests
from datetime import datetime

def fetch_weather_history(api_key, latitude, longitude, date):
    timestamp = int(date.timestamp())
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    params = {
        'lat': latitude,
        'lon': longitude,
        'dt': timestamp,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Print the entire API response for debugging
        print("API response:", data)
        
        # Check for 'data' key instead of 'hourly'
        if "data" not in data:
            error_message = data.get("message", "Unexpected response structure from API.")
            return {"error": error_message}
        
        # Extract the first available data point from 'data'
        weather_info = data["data"][0]  # Accessing the first entry in 'data'
        
        return {
            "temperature": weather_info.get("temp", "Data not available"),
            "weather": weather_info.get("weather", [{}])[0].get("description", "Data not available"),
            "timestamp": weather_info.get("dt", "Data not available"),
            "sunrise": weather_info.get("sunrise", "Data not available"),
            "sunset": weather_info.get("sunset", "Data not available")
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}




def weather_history_view(request):
    weather_data = None
    error = None
    
    if request.method == "POST":
        api_key = "2567f2a1cf4dec48d3e9a0fcf0457e37"  
        latitude = float(request.POST.get("latitude"))
        longitude = float(request.POST.get("longitude"))
        date_str = request.POST.get("date")
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            weather_data = fetch_weather_history(api_key, latitude, longitude, date)
            
            if "error" in weather_data:
                error = weather_data["error"]
                weather_data = None
                
        except ValueError:
            error = "Invalid date format. Please use YYYY-MM-DD."
    
    return render(request, "index.html", {"weather_data": weather_data, "error": error})
