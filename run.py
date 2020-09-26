#!/usr/bin/env python3

import redis, json

from flask import Flask
from flask import render_template, session, request, url_for
from flask_bootstrap import Bootstrap

from classes.kupi_scrapper import KupiScrapper
from utils.helpers import get_types_dict_from_redis, post_types_into_redis

# Create instance of flask object
# Invalidate cache after session is close
# Use bootstrap template system for flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
bootstrap = Bootstrap(app)

# Create redis connection to a server and automatically convert responses from `bytes` to `string`
client = redis.Redis(host='127.0.0.1', port=6379, charset='utf-8', decode_responses=True)


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/kupi/', defaults={'kupi_group': ''})
@app.route('/kupi/<path:kupi_group>')
def kupi(kupi_group):
	if not kupi_group:
		return render_template('kupi.html')

	kupi_components_dict = get_types_dict_from_redis(client, kupi_group)
	if not kupi_components_dict:
		if kupi_group == 'categories':
			kupi_scrapper = KupiScrapper()
			kupi_components_dict = kupi_scrapper.scrape_categories()
		elif kupi_group == 'shops':
			kupi_scrapper = KupiScrapper()
			kupi_components_dict = kupi_scrapper.scrape_shops()

	post_types_into_redis(client, kupi_components_dict, kupi_group)
	return render_template('kupi-types.html', kupi_components=kupi_components_dict, kupi_group=kupi_group)

@app.route('/kupi/items')
def items():
	kupi_scrapper = KupiScrapper()
	categories_dict = kupi_scrapper.scrape_categories()
	shops_dict = kupi_scrapper.scrape_shops()
	kupi_scrapper.scrape_items_by_categories_and_shops(categories_dict, shops_dict)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	return render_template('logout.html')

@app.route('/minigames/stopwatch')
def stopwatch():
	return render_template('stopwatch.html')


if __name__ == '__main__':
	app.run(debug=True)
