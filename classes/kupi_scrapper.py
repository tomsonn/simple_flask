#!/usr/bin/env python3

from utils.helpers import write_item_to_json

from bs4 import BeautifulSoup

import json
import requests

class KupiScrapper:
	"""
		Class providing scrapper of items (food & drinks) which are in discount
	"""

	def __init__(self):
		self.URL_BASE = 'https://www.kupi.cz'
		self.ENDPOINT_DISCOUNTS = '/slevy'
		self.ENDPOINT_LEAFLETS = '/letaky/hypermarkety-a-supermarkety'

	def get_html_from_url(self, url):
		try:
			response = requests.Session().get(url)
			response.raise_for_status()
			return response.text
		except Exception as e:
			print(f'Couldn\'t get HTML content of {url} endpoint.')

	def scrape_categories(self):
		URL_CATEGORIES = self.URL_BASE + self.ENDPOINT_DISCOUNTS
		categories_html = self.get_html_from_url(URL_CATEGORIES)

		try:
			soup = BeautifulSoup(categories_html, 'html.parser')
		except: 
			print('Couldn\'t scrape kupi.cz HTML to get categories.')

		# Div element with all categories
		categories_el_parent = soup.find_all('div', {'class': 'categories'})[0]
		# The name of the category
		category_el_key = categories_el_parent.findChildren('div', {'class': 'category_name'})
		# The URL endpoint for each respective category
		category_el_value = categories_el_parent.findChildren('a', {'class': 'category_item'})
		# The dictionary which stores the name of the each category as the key and 
		# URL endpoint as the value
		categories_dict = {key.text.strip(): value.get('href') for key, value in zip(category_el_key, category_el_value)}

		return categories_dict

	def scrape_shops(self):
		URL_SHOPS = self.URL_BASE + self.ENDPOINT_LEAFLETS
		shops_html = self.get_html_from_url(URL_SHOPS)

		try:
			soup = BeautifulSoup(shops_html, 'html.parser')
		except: 
			print('Couldn\'t scrape kupi.cz HTML to get shops.')

		# Div element with all the shops
		shops_el_parent = soup.find_all('ul', {'class': 'filter_items default_filter_items change_leaflet_list'})[0]
		# Element stores each shops separately
		shops_el = shops_el_parent.findChildren('a')
		# The dictionary which stores the name of the each shop as key and
		# URL endpoint as the value
		shops_dict = {el.get('data-shop-name'): el.get('href') for el in shops_el}

		return shops_dict

	def scrape_items_by_categories_and_shops(self, categories, shops):
		categories_endpoints_list = list(categories.values())
		shops_endpoints_list = [shop_endpoint.split('/')[-1] for shop_endpoint in shops.values()]

		URL_ITEMS = f'{self.URL_BASE}{categories_endpoints_list[0]}/{shops_endpoints_list[0]}?page=40'
		items_html = self.get_html_from_url(URL_ITEMS)
		try:
			soup = BeautifulSoup(items_html, 'html.parser')
		except: 
			print(f'Couldn\'t scrape kupi.cz HTML to get items from category {list(categories.keys())[0]} from {list(shops.keys())[0]}.')

		page_number = 1
		while True:
			items_el_parent = soup.find_all('div', {'class': 'group_discounts', 'data-page': f'{page_number}'})
			if not items_el_parent:
				break
			
			for item_el_parent in items_el_parent:
				item_el = item_el_parent.findChildren('div', {'class': 'log_product product_name wide'})[0]

				# TODO shops, price
				item_details = {
					'name': item_el.h2.a.get('title'),
					'amount': item_el.h2.span.text.strip(),
					'endpoint': item_el.h2.a.get('href'),
					'data-product': item_el.h2.a.get('data-product')
					# 'shops':
					# 'price':
				}
				print(item_details)
				write_item_to_json(item_details)

			page_number += 1
		

def main():
	kupi_scrapper = KupiScrapper()
	categories_dict = kupi_scrapper.scrape_categories()
	shops_dict = kupi_scrapper.scrape_shops()
	kupi_scrapper.scrape_items_by_categories_and_shops(categories_dict, shops_dict)

if __name__ == '__main__':
	main()
