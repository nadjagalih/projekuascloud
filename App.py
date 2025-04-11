from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Konfigurasi API Key (simpan di Environment Variables Azure)
API_KEY = os.getenv("OWM_API_KEY", "a90346e87e9508d1d91e71de81259971")  # Gunakan environment variable di Azure
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    default_city = "Jakarta"
    weather_data = get_weather_data(default_city)
    return render_template('index.html', weather=weather_data)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    weather_data = get_weather_data(city)
    return render_template('index.html', weather=weather_data)

def get_weather_data(city):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'id'
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'success': True
            }
        else:
            return {
                'error': data['message'],
                'success': False
            }
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Port harus sesuai dengan Azure