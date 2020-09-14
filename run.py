#!/usr/bin/env python3

from utils.helpers import get_random_number

from flask import Flask, render_template, session, request, url_for
from flask_bootstrap import Bootstrap

from classes.kupi_scrapper import KupiScrapper

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
bootstrap = Bootstrap(app)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/user/<user>')
def user(user):
	return render_template('user.html', user=user)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	return render_template('logout.html')

@app.route('/minigames/stopwatch')
def stopwatch():
	return render_template('stopwatch.html')

@app.route('/minigames/cheap-food', methods=['POST', 'GET'])
def cheap_food():
	kupi_scrapper = KupiScrapper()
	cat_resp = kupi_scrapper.scrape_categories()
	return render_template('cheap_food.html', response=cat_resp)


if __name__ == '__main__':
	app.run(debug=True)
