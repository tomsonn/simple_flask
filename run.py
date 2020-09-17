#!/usr/bin/env python3

from flask import Flask, render_template, session, request, url_for
from flask_bootstrap import Bootstrap

from classes.kupi_scrapper import KupiScrapper

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
bootstrap = Bootstrap(app)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/kupi/', defaults={'kupi_type': ''})
@app.route('/kupi/<path:kupi_type>')
def kupi(kupi_type):
	if not kupi_type:
		return render_template('kupi.html')
	if kupi_type == 'categories':
		kupi_scrapper = KupiScrapper()
		categories_dict = kupi_scrapper.scrape_categories()
		return render_template('kupi-cats.html', categories=categories_dict)
	elif kupi_type == 'shops':
		kupi_scrapper = KupiScrapper()
		shops_dict = kupi_scrapper.scrape_shops()
		return render_template('kupi-shops.html', shops=shops_dict)

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

@app.route('/minigames/cheap-food', methods=['POST', 'GET'])
def cheap_food():
	kupi_scrapper = KupiScrapper()
	cat_resp = kupi_scrapper.scrape_categories()
	return render_template('cheap_food.html', response=cat_resp)


if __name__ == '__main__':
	app.run(debug=True)
