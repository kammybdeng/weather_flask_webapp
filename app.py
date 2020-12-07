from decouple import config
import requests
from helper import kelvin_to_celsius, kelvin_to_fahrenheit, forecast_api_request
from flask import Flask, render_template, request

app = Flask(__name__)
API_KEY = config('API_KEY')
app.config['FLASK_DEBUG'] = config('FLASK_DEBUG')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/check_weather', methods=['GET'])
def check_weather():
	weather_dict = dict()
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
	response = requests.get(url).json()
	print()
	if response.get('cod') != 200:
		message = response.get('message', '')
		error_message = {'city': city.title(),
						 'message': message}
		return render_template('error.html', error_message=error_message)
	else:
		weather_dict = forecast_api_request(response, API_KEY)
	return render_template('weather.html', weather=weather_dict)

if __name__ == '__main__':
    app.run()