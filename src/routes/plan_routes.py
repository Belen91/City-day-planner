from flask import request, render_template
from services.events_service import get_events
from services.weather_service import get_weather_forecast

def register_plan_routes(app):
    
    @app.route('/plan', methods=['POST'])
    def plan():
        city = request.form['city']
        date = request.form['date']

        if not city:
            return render_template("index.html", error="Falta la ciudad")
        
        weather_data = get_weather_forecast(city, date)
        events_data  = get_events(date, city) if date else []

        if not weather_data and not events_data:
            return render_template('index.html', error = "No se han encontrado datos para esta ciudad")
        
        return render_template(
            'plan.html',
            weather = weather_data,
            city = city,
            date = date,
            events = events_data
        )