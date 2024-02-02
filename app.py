from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])

def get_weather():
    city = request.form.get('city')
    api_key = 'f1f994fcdeda4d401f29d4b433c3d16a'

    if not city:
        return 'Please enter a city.'

    try:
        location_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        location_response = requests.get(location_url)
        location_data = location_response.json()

        if location_response.status_code == 200:
            latitude = location_data['coord']['lat']
            longitude = location_data['coord']['lon']

            weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                temperature = weather_data['main']['temp']
                weather_text = weather_data['weather'][0]['description']

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                result = f"City: {city}<br>"
                result += f"Latitude: {latitude}<br>"
                result += f"Longitude: {longitude}<br>"
                result += f"Current Time: {current_time}<br>"
                result += f"Weather Forecast: {temperature}°C, {weather_text}"

                return result
            else:
                return 'Error fetching weather data.'
        else:
            return 'City not found.'

    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
