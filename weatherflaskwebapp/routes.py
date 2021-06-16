from decouple import config
import requests
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from weatherflaskwebapp import app, db, bcrypt
from weatherflaskwebapp.helper import forecast_api_request
from weatherflaskwebapp.forms import RegistrationForm, LoginForm, WeatherForm, SaveForm
from weatherflaskwebapp.models import User
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

		# if save_form.validate_on_submit():
		# 	return redirect(url_for('new_city', city=city))
		# return render_template('weather.html', weather=weather_dict, form=save_form)
	# elif save_form.validate_on_submit():
	# 	print('----here---')
		return redirect(url_for('new_city', weather=weather_dict))
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
	return render_template('account.html', title='Account')


@app.route('/new_city', methods=['GET', 'POST'])
@login_required
def new_city():
	form = SaveForm()
	weather = request.args.get('weather')
	weather = ast.literal_eval(weather)
	if form.validate_on_submit():
		# check if city is saved
		flash('City Saved!', 'success')
		return redirect(url_for('index'))
	return render_template('weather.html', weather=weather, form=form)
