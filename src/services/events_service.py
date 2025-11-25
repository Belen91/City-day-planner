import requests
from datetime import datetime, time
from utils.config import TICKETMASTER_API_KEY


#API sacada de https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/

base_url = "https://app.ticketmaster.com/discovery/v2/events.json"

def get_events(date, city, size=20):

    #comprobamos si date es un string. Si lo es, lo convierte a objeto de fecha real
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    start_date = datetime.combine(date, time.min).isoformat() + "Z"
    end_date = datetime.combine(date, time.max).isoformat() + "Z"
    
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city, 
        "startDateTime" : start_date,
        "endDateTime" : end_date,
        "size" : size, 
        "sort" : "date, asc"
    }
    
    response = requests.get(base_url, params=params, timeout=5) #añadir timeout siempre, request monta los parámetros sola.
    response.raise_for_status() #método de request que lanza un error automáticamente si la respuesta HTTP no es 200(OK)
    data = response.json()

    events = []
    for ev in data.get("_embedded", {}).get("events", []):
        events.append({
            "name" : ev.get("name"),
            "url" : ev.get("url"),
            "local_date" : ev["dates"]["start"].get("localDate"),
            "local_time" : ev["dates"]["start"].get("localTime"),
            "venue" : ev.get("_embedded", {}).get("venues",[{}])[0].get("name")
        })

    return events

