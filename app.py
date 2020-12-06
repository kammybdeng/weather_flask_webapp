from decouple import config
import requests
from helper import kelvin_to_celsius
from flask import Flask, render_template, request

app = Flask(__name__)
API_KEY = config('API_KEY')
print('load and this --- ', config('FLASK_DEBUG'))
app.config['FLASK_DEBUG'] = config('FLASK_DEBUG')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/check_weather', methods=['GET'])
def check_weather():
	city = request.args.get('cityname')
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY)
	response = requests.get(url).json()
	#print(url)
	# response = {"base": "stations", "clouds": {"all": 75}, "cod": 200, "coord": {"lat": 40.71, "lon": -74.01}, "dt": 1607137692,
	# 	 "id": 5128581, "main": {"feels_like": 276, "humidity": 93, "pressure": 1016, "temp": 280.15, "temp_max": 280.93,
	# 							 "temp_min": 279.26}, "name": "New York",
	# 	 "sys": {"country": "US", "id": 4610, "sunrise": 1607083462, "sunset": 1607117337, "type": 1}, "timezone": -18000,
	# 	 "visibility": 10000, "weather": [{"description": "broken clouds", "icon": "04n", "id": 803, "main": "Clouds"}],
	# 	 "wind": {"deg": 220, "speed": 4.6}}
	#city = 'New York'
	if response.get('cod') != 200:
		message = response.get('message', '')
		return f'Error getting temperature for {city.title()}. Error message = {message}'
	else:
		weather = {
		'city' : city.title(),
		'temperature': kelvin_to_celsius(response['main']['feels_like']),
		'description': response['weather'][0]['description']
		}

	return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads" our
    # web app if we change the code.
    app.run()