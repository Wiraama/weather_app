""" weather web """
from flask import *
import requests
from flask_sqlalchemy import *
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    api_key = "979faf83d5c0e1b8d85d65d0dd7a0967"
    city = "London"
    if request.method == 'POST':
        city = request.form.get('search', city)
    baseurls = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    data_full = requests.get(baseurls)
    data = data_full.json()
    timestamp = data["dt"]
    date_time = datetime.fromtimestamp(timestamp)
    day = date_time.strftime("%A")
    month = date_time.strftime("%B")
    date = date_time.strftime("%d")
    to_app = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "weather": data["weather"][0]["main"],
        "icon": data["weather"][0]["icon"],
        "temp": int(data["main"]["temp"] - 273),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "pressure": float(data["main"]["pressure"] * 0.000987),
        "visibility": int(data["visibility"] / 1000),
        "day": day,
        "date": date,
        "month": month
    }
    return render_template("home.html", to_app=to_app)


if __name__ == '__main__':
    app.run(debug=True)