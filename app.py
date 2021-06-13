from decouple import config
import requests
from flask import Flask, render_template, request, flash, redirect, url_for

from helper import forecast_api_request
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
API_KEY = config('API_KEY')
app.config['FLASK_DEBUG'] = config('FLASK_DEBUG')
app.config['SECRET_KEY'] = config('SECRET_KEY')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('index'))
		else:
			flash('Login Unsuccessful.', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route('/check_weather', methods=['GET'])
def check_weather():
	weather_dict = dict()
	default_state = 'CA'
	default_country = 'US'
	city = request.args.get('cityname').strip()
	state = request.args.get('statename').strip()
	country = request.args.get('countryname').strip()
	if city == '':
		message = 'Please provide a city name'
		error_message = {
			'city': city.title(),
			'message': message
		}
		return render_template('error.html', error_message=error_message)
	if state == '' and country.lower() == 'us':
		state = default_state
	if country == '':
		country = default_country
	url = 'http://api.openweathermap.org/data/2.5/weather?q={},{},{}&appid={}'.format(
		city,
		state,
		country,
		API_KEY
	)
	response = requests.get(url).json()
	if response.get('cod') != 200:
		message = response.get('message', '')
		error_message = {
			'city': city.title(),
			'message': message
		}
		return render_template('error.html', error_message=error_message)
	else:
		weather_dict = forecast_api_request(response, API_KEY)
	return render_template('weather.html', weather=weather_dict)


if __name__ == '__main__':
	app.run()
