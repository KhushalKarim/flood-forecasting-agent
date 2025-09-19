def flood_risk(temp, humidity, condition, wind_speed):
    """
    Calculate flood risk based on weather.
    Returns 'High', 'Medium', or 'Low'.
    """
    condition_lower = condition.lower()
    if "rain" in condition_lower and humidity > 70:
        return "High"
    elif humidity > 80:
        return "Medium"
    elif wind_speed > 50:
        return "Medium"
    else:
        return "Low"
