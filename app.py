from decouple import config
import requests
from helper import kelvin_to_celsius, kelvin_to_fahrenheit
from flask import Flask, render_template, request

app = Flask(__name__)
API_KEY = config('API_KEY')
app.config['FLASK_DEBUG'] = config('FLASK_DEBUG')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/check_weather', methods=['GET'])
def check_weather():
	default_state = 'CA'
	default_country = 'US'
	city = request.args.get('cityname')
	state= request.args.get('statename')
	country = request.args.get('countryname')
	if city == '':
		message = 'Please provide a city name'
		error_message = {'city': city.title(),
						 'message': message}
		return render_template('error.html', error_message=error_message)
	if state == '' and country.lower()=='us':
		state = default_state
	if country == '':
		country = default_country
	url = 'http://api.openweathermap.org/data/2.5/weather?q={},{},{}&appid={}'.format(city, state, country, API_KEY)
	#response = requests.get(url).json()
	response = {'coord': {'lon': -122.42, 'lat': 37.77}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 282.7, 'feels_like': 277.89, 'temp_min': 281.48, 'temp_max': 284.15, 'pressure': 1026, 'humidity': 81}, 'visibility': 10000, 'wind': {'speed': 5.7, 'deg': 300}, 'clouds': {'all': 20}, 'dt': 1607229456, 'sys': {'type': 1, 'id': 5817, 'country': 'US', 'sunrise': 1607181044, 'sunset': 1607215848}, 'timezone': -28800, 'id': 5391959, 'name': 'San Francisco', 'cod': 200}
	print(response)
	if response.get('cod') != 200:
		message = response.get('message', '')
		error_message = {'city': city.title(),
						 'message': message}
		return render_template('error.html', error_message=error_message)
	else:
		weather = {
		'city' : response['name'].title(),
		'state': state.upper(),
		'country': response['sys']['country'].upper(),
		'celsius': kelvin_to_celsius(response['main']['feels_like']),
		'fahrenheit': kelvin_to_fahrenheit(response['main']['feels_like']),
		'description': response['weather'][0]['description']
		}

	return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    app.run()