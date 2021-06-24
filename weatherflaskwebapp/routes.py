from decouple import config
import requests
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from weatherflaskwebapp import app, db, bcrypt
from weatherflaskwebapp.helper import forecast_api_request
from weatherflaskwebapp.forms import RegistrationForm, LoginForm, WeatherForm
from weatherflaskwebapp.models import User, City


API_KEY = config('API_KEY')


@app.route('/')
def index():
	return redirect(url_for('home'))


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
	
	if current_user.is_authenticated:
		user = User.query.filter_by(id=current_user.id).first()
		user_cities = user.cities
		if city.lower() in [c.name.lower() for c in user_cities]:
			weather_dict['saved'] = True
	
	return jsonify(weather_dict)


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




