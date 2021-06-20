from decouple import config
import requests
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from weatherflaskwebapp import app, db, bcrypt
from weatherflaskwebapp.helper import forecast_api_request
from weatherflaskwebapp.forms import RegistrationForm, LoginForm, WeatherForm, SaveForm, UnSaveForm
from weatherflaskwebapp.models import User, City
import ast


API_KEY = config('API_KEY')


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
			if city not in [c.name for c in user_cities]:
				return redirect(url_for('add_city', weather=weather_dict))
			else:
				return redirect(url_for('remove_city', weather=weather_dict))
	return render_template('index.html', title='Index', form=form)


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
	# cities = User.query.filter_by(id=current_user.id).first().cities
	cities = City.query.filter_by(user_id=current_user.id).all()
	return render_template('account.html', title='Account', cities=cities)


@app.route('/new_city', methods=['GET', 'POST'])
def add_city():
	form = SaveForm()
	weather = request.args.get('weather')
	weather = ast.literal_eval(weather)

	if form.validate_on_submit():
		# check if city is saved
		city = weather.get('current')[0].get('city')
		user = User.query.filter_by(id=current_user.id).first()
		# user_cities = user.cities
		# if city not in [c.name for c in user_cities]:
		saved_city = City(name=city, user_id=user.id)
		db.session.add(saved_city)
		db.session.commit()
		flash('City Saved!', 'success')
		return redirect(url_for('account'))
	return render_template('weather.html', weather=weather, form=form)


@app.route('/remove_city', methods=['GET', 'POST'])
def remove_city():
	form = UnSaveForm()
	weather = request.args.get('weather')
	weather = ast.literal_eval(weather)
	if form.validate_on_submit():
		city = weather.get('current')[0].get('city')
		City.query.filter_by(name=city, user_id=current_user.id).delete()
		db.session.commit()
		flash('City Unsaved!', 'danger')
		return redirect(url_for('account'))
	return render_template('weather.html', weather=weather, form=form)


@app.route('/testing', methods=['GET', 'POST'])
def testing():
	return render_template('form.html')


@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']
	name = request.form['name']
	if name and email:
		newName = name[::-1]
		return jsonify({'name': newName})

	return jsonify({'error': 'MISSING data!'})
	