#!/usr/bin/env python3

import json
import redis

from flask import Flask
from flask import render_template, session, request, url_for
from flask_bootstrap import Bootstrap

from classes.kupi_scrapper import KupiScrapper
from utils.helpers import (get_dict_from_redis,
						   store_subcategories_into_redis,
						   store_types_into_redis)

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
	"""
		Format of categories / shops dictionaries in Redis DB:

		CATEGORIES:

		'categories:{category_name_serialized}': {
			'ID': ID,
			'name': category_name_deserialized,
			'data_category': category_name_serialized,
			'endpoint': category_endpoint
		}

		SHOPS: 

		'shops:{shop_name_serialized}': {
			'ID': ID,
			'name': shop_name_deserialized,
			'data_shops': shop_name_serialized,
			'endpoint': shop_endpoint
		}
	"""

	# Render "homepage" of Kupi Scrapper app, if endpoint to kupi-group is not provided
	if not kupi_group:
		return render_template('kupi.html')

	# Try to get list of components (shops / categories) from Redis DB. If the list is empty
	# do a web scrapping
	pattern = f'{kupi_group}*'
	kupi_components_dict = get_dict_from_redis(client, pattern)
	if not kupi_components_dict:
		kupi_scrapper = KupiScrapper()
		if kupi_group == 'categories':
			kupi_components_dict = kupi_scrapper.scrape_categories()
		elif kupi_group == 'shops':
			kupi_components_dict = kupi_scrapper.scrape_shops()

	store_types_into_redis(client, kupi_components_dict, kupi_group)
	return render_template('kupi-group.html', kupi_components=kupi_components_dict, kupi_group=kupi_group)

@app.route('/kupi/subcategories')
def subcategories():
	"""
		Format of subcategories dictionaries in Redis DB:

		'subcategories:{category_name_serialized}:{subcategory_name_serialized}' : {
			'ID': ID
			'name': subcategory_name_deserialized,
			'data_category': subcategory_name_serialized,
			'endpoint': subcategory_endpoint,
			'category': category_name_serialized
		}

	"""

	# Get category endpoint query parameter which we want to get subcategories from
	kupi_group = 'subcategories'
	category_endpoint = request.args.get('category_endpoint')
	category_name_serialized = category_endpoint.split('/')[-1]
	category_name_deserialized = client.hget(f'categories:{category_name_serialized}', 'name') or 'Unknown'

	# Try to get list of subcategories from Redis DB. If the list is empty, proceed to website scrapping
	pattern = f'subcategories:{category_name_serialized}:*'
	subcategories_list = client.keys(pattern=pattern)
	subcategories_from_one_category_dict = {}
	if subcategories_list:
		# Go thourgh every subcategory from desired category and store its `name` and `endpoint` into dictionary
		for subcategory in subcategories_list:
			subcategory_dict = client.hgetall(subcategory)
			name = subcategory_dict['name']
			endpoint = subcategory_dict['endpoint']
			subcategories_from_one_category_dict[name] = endpoint
	else:
		kupi_scrapper = KupiScrapper()
		subcategories_from_all_categories_dict = kupi_scrapper.scrape_subcategories(category_endpoint)
		subcategories_from_one_category_dict = store_subcategories_into_redis(client,
																			  subcategories_from_all_categories_dict,
																			  category_name_serialized)

	return render_template('kupi-group.html',
							kupi_components=subcategories_from_one_category_dict,
							kupi_group=kupi_group,
							category=category_name_deserialized)

@app.route('/kupi/items')
def items():
	"""
		Format of items dictionaries in Redis DB:

		'items:{category_name_srialized}:{subcategory_name_serialized}:{item_name_serialized}' : {
			'ID': ID
			'name': item_name_deserialized,
			'data_product': item_name_serialized,
			'category': category_name_serialized,
			'subcategory': subcategory_name_serialized,
			'endpoint': item_endpoint,
			
			TODO -> 'amount', 'shops', 'price' ... Decide whetere stored with general items info or in separate "table"
		}
	"""

	kupi_group = 'items'
	subcategory_endpoint = request.args.get('subcategory_endpoint')
	subcategory_name_serialized = subcategory_endpoint.split('/')[-1]

	# `subcategory_key` -> key in Redis DB where are stored informations about desired subcategory
	subcategory_pattern = f'subcategories:*:{subcategory_name_serialized}'
	subcategory_keys_list = client.keys(pattern=subcategory_pattern)
	if len(subcategory_keys_list) == 1:
		category_name_deserialized = client.hget(subcategory_keys_list[0], 'name')
		category_name_serialized = client.hget(subcategory_keys_list[0], 'data_category')
		subcategory_name_serialized = client.hget(subcategory_keys_list[0], 'data_category')
	else:
		pass

	# If it's not in Redis DB
	kupi_scrapper = KupiScrapper()
	# TODO -> if there are no items in discount return smth like 404 not found or whatever
	# TODO -> Store items into Redis DB
	# items are in format -> list[0][n]. n -> number of pages 
	items_list = kupi_scrapper.scrape_all_items_by_subcategory(subcategory_endpoint)
	items_dict = {}
	for page in items_list:
		for item in page:
			name = item['name']
			amount = item['amount']
			endpoint = item['endpoint']
			shops = item['shops']
			items_dict[name] = {'amount': amount,
								'endpoint': endpoint,
								'shops': shops}
								
	print(json.dumps(items_list, indent=4))
	return render_template('kupi-group.html',
						    kupi_group=kupi_group,
						    kupi_components=items_dict,
						    subcategory=category_name_deserialized)

	items_list = client.keys()
	items_list = client.keys(pattern=pattern)
	pattern = f'items:{subcategory_name_endpoint}:*'
	
	categories_dict = kupi_scrapper.scrape_categories()
	shops_dict = kupi_scrapper.scrape_shops()
	

	return render_template('kupi-group.html', kupi_group=kupi_group, subcategory=category_name_serialized)

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
	app.run(debug=True, host='0.0.0.0')
