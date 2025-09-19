from weather_api import get_coordinates, get_forecast
from risk_calculator import flood_risk

def flood_agent(place_name):
    """Return forecast + flood risk for the main location"""
    lat, lon = get_coordinates(place_name)
    if lat is None:
        return {"error": "Place not found"}

    main_forecast = get_forecast(lat, lon)
    if not main_forecast:
        return {"error": "Failed to fetch forecast data"}

    # Add flood risk to each day
    for day in main_forecast:
        day["flood_risk"] = flood_risk(
            day["temp"], day["humidity"], day["condition"], day["wind_speed"]
        )

    return {
        "place_name": place_name,
        "lat": lat,
        "lon": lon,
        "main_forecast": main_forecast
    }
