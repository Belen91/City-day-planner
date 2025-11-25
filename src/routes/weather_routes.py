from flask import request, render_template
from services.weather_service import get_weather

def register_weather_routes(app):

    @app.route('/weather', methods=['POST'])
    def weather():
        city = request.form['city']
        weather_data = get_weather(city)

        if weather_data:
            return render_template('weather.html', weather=weather_data, city=city)
        else:
            return render_template('index.html', error= "Ciudad no encontrada")