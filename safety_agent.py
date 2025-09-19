from weather_api import get_forecast, get_nearby_coordinates
from risk_calculator import flood_risk
import requests

GEOCODE_REVERSE_URL = "http://api.openweathermap.org/geo/1.0/reverse"
API_KEY = "37cdce747ffe1fdaa0ea943c23646b00"

def get_place_name(lat, lon):
    """Get place name from lat/lon using reverse geocoding"""
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": API_KEY}
    response = requests.get(GEOCODE_REVERSE_URL, params=params)
    if response.status_code == 200 and response.json():
        return response.json()[0].get("name", "")
    return f"{round(lat, 2)}, {round(lon, 2)}"

def safety_agent(lat, lon):
    """Find safer nearby locations around a point"""
    nearby_coords = get_nearby_coordinates(lat, lon)
    nearby_forecasts = []

    for nlat, nlon in nearby_coords:
        forecast = get_forecast(nlat, nlon)
        if forecast:
            avg_risk = max([
                flood_risk(f["temp"], f["humidity"], f["condition"], f["wind_speed"])
                for f in forecast
            ])
            name = get_place_name(nlat, nlon)
            nearby_forecasts.append({
                "lat": nlat,
                "lon": nlon,
                "flood_risk": avg_risk,
                "name": name
            })

    # Safest nearby = lowest risk
    safe_nearby = sorted(
        nearby_forecasts, key=lambda x: ["Low", "Medium", "High"].index(x["flood_risk"])
    )[0] if nearby_forecasts else None

    return {
        "nearby_forecasts": nearby_forecasts,
        "safe_nearby": safe_nearby
    }
