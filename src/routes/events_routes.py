from flask import request, render_template
from services.events_service import get_events
from services.weather_service import get_weather

def register_events_routes(app):
    @app.route('/events', methods=['POST'])
    def events():
        city = request.form['city']
        date = request.form['date']

        weather_data = get_weather(city)
        events_data  = get_events(date, city)

        if not weather_data and not events_data:
            return render_template('index.html', error = "No se han encontrado datos para esta ciudad")
        
        return render_template(
            'plans.html',
            weather = weather_data,
            city = city, 
            date = date, 
            events = events_data
        )