import requests

API_KEY = "37cdce747ffe1fdaa0ea943c23646b00"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_coordinates(place_name):
    """Convert a place name to latitude and longitude using OpenWeather Geocoding API"""
    params = {"q": place_name, "limit": 1, "appid": API_KEY}
    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data["lat"], data["lon"]
    return None, None

def get_forecast(lat, lon):
    """Fetch 5-day forecast (3-hour intervals) and aggregate daily"""
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": API_KEY
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    daily_forecasts = {}

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        wind_speed = entry["wind"]["speed"]
        condition = entry["weather"][0]["description"]

        if date not in daily_forecasts:
            daily_forecasts[date] = {"temps": [], "humidities": [], "wind_speeds": [], "conditions": []}

        daily_forecasts[date]["temps"].append(temp)
        daily_forecasts[date]["humidities"].append(humidity)
        daily_forecasts[date]["wind_speeds"].append(wind_speed)
        daily_forecasts[date]["conditions"].append(condition)

    forecasts = []
    for date, values in daily_forecasts.items():
        forecasts.append({
            "date": date,
            "temp": round(sum(values["temps"]) / len(values["temps"]), 1),
            "humidity": round(sum(values["humidities"]) / len(values["humidities"]), 1),
            "wind_speed": round(sum(values["wind_speeds"]) / len(values["wind_speeds"]), 1),
            "condition": max(set(values["conditions"]), key=values["conditions"].count),
            "lat": lat,
            "lon": lon
        })
    return forecasts

def get_nearby_coordinates(lat, lon, radius_km=20, step_km=5):
    """Generate nearby coordinates around a point"""
    nearby = []
    for dlat in range(-radius_km, radius_km+1, step_km):
        for dlon in range(-radius_km, radius_km+1, step_km):
            nearby.append((lat + dlat*0.009, lon + dlon*0.012))  # approx degree conversion
    return nearby
