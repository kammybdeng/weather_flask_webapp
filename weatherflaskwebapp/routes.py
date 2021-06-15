from decouple import config
import requests
from flask import render_template, request, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from weatherflaskwebapp import app, db, bcrypt
from weatherflaskwebapp.helper import forecast_api_request
from weatherflaskwebapp.forms import RegistrationForm, LoginForm
from weatherflaskwebapp.models import User


API_KEY = config('API_KEY')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,
					email=form.email.data,
					password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}! '
			  f'You are now able to login', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash('You have been logged in!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash('Login Unsuccessful.', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
	return render_template('account.html', title='Account')


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