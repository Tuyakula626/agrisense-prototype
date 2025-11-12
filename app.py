from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to AgriSense API 🌾"})

@app.route('/api/weather', methods=['GET'])
def get_weather():
    region = request.args.get('region', 'Windhoek')  # default city
    url = f"https://api.openweathermap.org/data/2.5/weather?q={region},NA&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Failed to fetch weather")}), 400

        result = {
            "region": region,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

