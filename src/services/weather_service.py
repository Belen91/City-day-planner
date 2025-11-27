import requests
from utils.config import OPENWEATHER_API_KEY
from datetime import datetime, date as date_cls



#API sacada de https://openweathermap.org/api
current_url = "http://api.openweathermap.org/data/2.5/weather"
forecast_url= "http://api.openweathermap.org/data/2.5/forecast"

def get_weather(city):
    """tiempo actual en una ciudad."""
    params = {
        "q" : city,
        "appid" : OPENWEATHER_API_KEY,
        "units" : "metric",
        "lang" : "es",
    }
    
    response = requests.get(current_url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()
    
    main = data['main']
    wind = data ['wind']
    weather_description = data['weather'] [0] ['description']

    return  {
            'temperature' : main['temp'],
            'pressure' : main['pressure'],
            'humidity' : main ['humidity'],
            'wind_speed' : wind['speed'],
            'description' : weather_description
    }


def get_weather_forecast(city: str, date:str):
    """
    Tiempo aproximado para una fecha concreta:
        - Definimos variables de fecha (hoy o fecha proxima)
        - Si no hay fecha o la fecha es de hoy, entonces usamos la función de arriba.
        - Sino, usamos forecast, que funciona por slots[]. 
    """
    today = date_cls.today()
    if not date:
        return get_weather(city)
    
    target_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    if target_date == today:
        return get_weather(city)
    
    if target_date < today:
        return None
    
    params = {
        "q" : city,
        "appid" : OPENWEATHER_API_KEY,
        "units" : "metric",
        "lang" : "es",
    }
    
    response = requests.get(forecast_url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    slots = []
    for item in data.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        if dt.date() == target_date:  
            slots.append({
                "time": dt.strftime("%H:%M"),
                "temperature" :item["main"]["temp"],
                "feels_like" : item["main"]["feels_like"],
                "description": item["weather"][0]["description"],
                "pressure" : item["main"].get("pressure"),
                "humidity" : item["main"].get("humidity"),
                "wind_speed" : item.get("wind",{}).get("speed")
            })

    if not slots: 
        return None

    summary_slot = next(
        (s for s in slots if s["time"].startswith("12")),
        slots[0]
    )
    

    return  {
            'temperature' : summary_slot['temperature'],
            'pressure' : summary_slot['pressure'],
            'humidity' : summary_slot ['humidity'],
            'wind_speed' : summary_slot['wind_speed'],
            'description' : summary_slot['description'],
            'time': summary_slot['time'],
            'slots' : slots
    }