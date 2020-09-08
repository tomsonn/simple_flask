#!/usr/bin/env python3

from utils.helpers import get_random_number

from flask import Flask, render_template, session, request, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/user/<user>')
def user(user):
	return render_template('user.html', user=user)

@app.route('/minigames/stopwatch', methods=['POST', 'GET'])
def stopwatch():
	generated_number = 0
	if 'sw_start_btn' in request.form:
		generated_number = get_random_number()
	elif 'sw_stop_btn' in request.form:
		generated_number = get_random_number() + 10.0

	return render_template('stopwatch.html', generated_number=generated_number)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	return render_template('logout.html')


if __name__ == '__main__':
	app.run(debug=True)
