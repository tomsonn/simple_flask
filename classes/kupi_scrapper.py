#!/usr/bin/env python3

from bs4 import BeautifulSoup

import json
import requests

class KupiScrapper:

	def __init__(self):
		self.URL_BASE = 'https://www.kupi.cz'
		self.categories_endpoint = '/slevy'

	def get_categories_html(self):
		URL_CATEGORIES = self.URL_BASE + self.categories_endpoint

		try:
			response = requests.Session().get(URL_CATEGORIES)
			response.raise_for_status()
			return response.text
		except Exception as e:
			print(f'Couldn\'t get HTML content of {URL_CATEGORIES} endpoint.')

	def scrape_categories(self):
		categories_html = self.get_categories_html()

		try:
			soup = BeautifulSoup(categories_html, 'html.parser')
		except: 
			print('Couldn\'t scrape kupi.cz HTML with categories.')

		# Div element with all categories
		categories_el_parent = soup.find_all('div', {'class': 'categories'})[0]
		# The name of the category
		category_el_key = categories_el_parent.findChildren('div', {'class': 'category_name'})
		# The URL endpoint for each respective category
		category_el_value = categories_el_parent.findChildren('a', {'class': 'category_item'})
		# The dictionary which stores the name of the each category as the key and 
		# URL endpoint as value
		categories_dict = {key.text.strip(): value.get('href') for key, value in zip(category_el_key, category_el_value)}

		return categories_dict

def main():
	kupi_scrapper = KupiScrapper()
	categories_dict = kupi_scrapper.scrape_categories()

if __name__ == '__main__':
	main()
