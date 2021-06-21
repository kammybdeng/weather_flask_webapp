from decouple import config
import requests
from flask import render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from weatherflaskwebapp import app, db, bcrypt
from weatherflaskwebapp.helper import forecast_api_request
from weatherflaskwebapp.forms import RegistrationForm, LoginForm, WeatherForm, SaveForm, UnSaveForm
from weatherflaskwebapp.models import User, City
import ast


API_KEY = config('API_KEY')


# @app.route('/', methods=['GET', 'POST'])
# def index():
# 	form = WeatherForm()
# 	if form.validate_on_submit():
# 		countrycode = 'us'
# 		if not form.city.data and not form.zipcode.data:
# 			error_message = {
# 				'message': 'Please Fill In At Least One Field'
# 			}
# 			return render_template('error.html', title='Error', error_message=error_message)
# 		elif form.city.data:
# 			city = form.city.data.strip()
# 			url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
# 		elif form.zipcode.data:
# 			zipcode = form.zipcode.data.strip()
# 			url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={API_KEY}"
# 		response = requests.get(url).json()
# 		if response.get('cod') != 200:
# 			message = response.get('message', '')
# 			error_message = {
# 				'message': message
# 			}
# 			return render_template('error.html', title='Error', error_message=error_message)
# 		else:
# 			weather_dict = forecast_api_request(response, API_KEY)
# 			city = weather_dict.get('current')[0].get('city')
# 			user = User.query.filter_by(id=current_user.id).first()
# 			user_cities = user.cities
# 			# check if city is saved
# 			if city not in [c.name for c in user_cities]:
# 				return redirect(url_for('add_city', weather=weather_dict))
# 			else:
# 				return redirect(url_for('remove_city', weather=weather_dict))
# 	return render_template('index.html', title='Index', form=form)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = WeatherForm()
	if form.validate_on_submit():
		countrycode = 'us'
		if not form.city.data and not form.zipcode.data:
			error_message = {
				'message': 'Please Fill In At Least One Field'
			}
			return render_template('error.html', title='Error', error_message=error_message)
		elif form.city.data:
			city = form.city.data.strip()
			url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
		elif form.zipcode.data:
			zipcode = form.zipcode.data.strip()
			url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={API_KEY}"
		response = requests.get(url).json()
		if response.get('cod') != 200:
			message = response.get('message', '')
			error_message = {
				'message': message
			}
			return render_template('error.html', title='Error', error_message=error_message)
		else:
			weather_dict = forecast_api_request(response, API_KEY)
			city = weather_dict.get('current')[0].get('city')
			user = User.query.filter_by(id=current_user.id).first()
			user_cities = user.cities
			# check if city is saved
			print('weather_dict------', weather_dict)
			if city not in [c.name for c in user_cities]:
				return redirect(url_for('add_city', weather=weather_dict))
			else:
				return redirect(url_for('remove_city', weather=weather_dict))
	return render_template('home.html', title='Home', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash('You have been logged in!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
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
	# cities = User.query.filter_by(id=current_user.id).first().cities
	cities = City.query.filter_by(user_id=current_user.id).all()
	return render_template('account.html', title='Account', cities=cities)


@app.route('/save_city', methods=['GET', 'POST'])
def save_city():
	if current_user.is_authenticated:
		# check if city is saved
		city = request.form.get('city')
		user = User.query.filter_by(id=current_user.id).first()
		user_cities = user.cities
		if city not in [c.name for c in user_cities]:
			saved_city = City(name=city, user_id=user.id)
			db.session.add(saved_city)
			db.session.commit()
		flash('City Saved!', 'success')
	else:
		flash('Please Login First!', 'danger')
	return redirect(url_for('home'))
	# return render_template('weather.html', weather=weather, form=form)


@app.route('/unsave_city', methods=['GET', 'POST'])
def unsave_city():
	if current_user.is_authenticated:
		# check if city is saved
		city = request.form.get('city')
		user = User.query.filter_by(id=current_user.id).first()
		user_cities = user.cities
		if city in [c.name for c in user_cities]:
			City.query.filter_by(name=city, user_id=current_user.id).delete()
			db.session.commit()
			flash('City Unsaved!', 'danger')
	else:
		flash('Please Login First!', 'danger')
	return redirect(url_for('home'))
	#return render_template('weather.html', weather=weather, form=form)


# @app.route('/testing', methods=['GET', 'POST'])
# def testing():
# 	return render_template('form.html')
#
#
# @app.route('/process', methods=['POST'])
# def process():
# 	email = request.form['email']
# 	name = request.form['name']
# 	if name and email:
# 		newName = name[::-1]
# 		return jsonify({'name': newName})
#
# 	return jsonify({'error': 'MISSING data!'})


@app.route('/home', methods=['GET', 'POST'])
def home():
	form = WeatherForm()
	return render_template('home.html', form=form)


@app.route('/fetch', methods=['POST', 'GET'])
def fetch():
	city = request.form['city']
	#zipcode = request.form['zipcode']
	countrycode = 'us'
	zipcode = ''

	if not city and not zipcode:
		return jsonify({'error': 'Please Fill In At Least One Field'})

	elif city:
		city = city.strip()
		url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
	# elif zipcode:
	# 	zipcode = zipcode.strip()
	# 	url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={API_KEY}"

	# OpenWeather response
	response = requests.get(url).json()
	if response.get('cod') != 200:
		message = response.get('message', '')
		return jsonify({'error': message})
	else:
		weather_dict = forecast_api_request(response, API_KEY)
		# city = weather_dict.get('current').get('city')


	# weather_dict = {'current': {'city': 'Boston', 'country': 'US', 'celsius': 31, 'fahrenheit': 89, 'uvi': 4.09, 'description': 'broken clouds', 'iconcode': 803, 'datetime': '06/21 09:10'}, 
	# 'forecast': [{'datetime': '06/21', 'celsius': 31, 'fahrenheit': 89, 'uvi': 8.45}, {'datetime': '06/22', 'celsius': 26, 'fahrenheit': 78, 'uvi': 6.55}, {'datetime': '06/23', 'celsius': 21, 'fahrenheit': 70, 'uvi': 8.14}, {'datetime': '06/24', 'celsius': 24, 'fahrenheit': 76, 'uvi': 8.13}, {'datetime': '06/25', 'celsius': 22, 'fahrenheit': 73, 'uvi': 8.99}]}
	
	if current_user:
		user = User.query.filter_by(id=current_user.id).first()
		user_cities = user.cities
		if city.lower() in [c.name.lower() for c in user_cities]:
			weather_dict['saved'] = True

	
	#print('weather_dict', weather_dict)
	return jsonify(weather_dict)


