from flask import Flask, render_template
from routes.weather_routes import register_weather_routes
from routes.plan_routes import register_plan_routes

  
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

register_plan_routes(app)
register_weather_routes(app)


if __name__ == "__main__":
    app.run(debug=True)
