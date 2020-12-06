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
	#print('print this', type(state), type(country))
	if state == '' and country.lower()=='us':
		state = default_state
	if country == '':
		country = default_country
	url = 'http://api.openweathermap.org/data/2.5/weather?q={},{},{}&appid={}'.format(city, state, country, API_KEY)
	response = requests.get(url).json()
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