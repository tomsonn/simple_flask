#!/usr/bin/env python3

from classes.exceptions import PageNumberNotFoundError
from utils.helpers import write_item_to_json

from bs4 import BeautifulSoup

import json
import re
import requests
import sys


class KupiScrapper:
	"""
		Class providing scrapper of items (food & drinks) which are in discount
	"""

	def __init__(self):
		self.URL_BASE = 'https://www.kupi.cz'
		self.ENDPOINT_DISCOUNTS = '/slevy'
		self.ENDPOINT_LEAFLETS = '/letaky/hypermarkety-a-supermarkety'

	def get_html_from_url(self, url):
		"""
			Returns HTML file from desired endpoint as a string
		"""

		try:
			response = requests.Session().get(url)
			response.raise_for_status()
			return response.text
		except Exception as e:
			print(f'Couldn\'t get HTML content of {url} endpoint.')

	def scrape_categories(self):
		"""
			Scrape categories from `slevy` endpoint.
			Return dictionary of categories in following format:
			{
				name_of_the_category [str] -> decoded name 	  :	`endpoint` [str] -> endpoint to
										  of the category 						discounts in desired shops																	
			}
		"""

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
		"""
			Scrape shops from `hypermarkety-a-supermarkety` endpoint.
			It's only including shops which sell food or drinks.
			Returns dictionary in following format:
			{
				`name_of_the_shop` [str] -> decoded name : `endpoint` [str] -> endpoint to discounts
										    of the shop 					   in desired shops.
			}
		"""

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

	def scrape_subcategories(self, categories):
		"""
			Scrape subcategories of each category
			Returns dictionary with categories and each category
			has list of other dictionaries mentioned below as its value.
			Dictionaries in list as value of each category is in following format: 
			{
				'name': `name` [str] -> Name in decoded format
				'data-category': `raw_name` [str] -> Name in raw format
				'endpoint': `href` [str] -> endpoint to discounts in desired subcategory
			}
		"""

		URL_SUBCATEGORIES = self.URL_BASE + list(categories.values())[0]
		subcategories_html = self.get_html_from_url(URL_SUBCATEGORIES)

		try:
			soup = BeautifulSoup(subcategories_html, 'html.parser')
		except: 
			print('Couldn\'t scrape kupi.cz HTML to get subcategories.')

		subcategories_dict = {}
		# Find all `unordered_list` elements with datatype: `subcategory`
		subcategories_el_parent = soup.find_all('ul', {'role': 'menu', 'data-type': 'subcategory'})
		for subcategory_el_parent in subcategories_el_parent:
			category = subcategory_el_parent.get('data-category')
			# Add key to dictionary with all of the values described above
			subcategories_dict[category] = [{'name': sc_name.a.text,
											 'data-category': sc_name.get('data-category'), 
											 'endpoint': sc_name.a.get('href')}
											   for sc_name in subcategory_el_parent.findChildren('li')
											   if sc_name.get('data-category') != 'vse']
		
		return subcategories_dict

	def scrape_items_from_html(self, soup, actual_iteration_of_page):
		"""
			From provided soup object, scrape page number and compare it with actual iteration of
			items scraping.
			If the actual iteration and page number equals, continue with scraping.
			Otherwise break from infinite loop and try to write every scraped information (dictionary)
			into JSON object.
		"""

		div_el = soup.find_all('div', {'class': 'relative right list_around right_side'})[0]
		page_number_el = str(div_el.find_next_siblings('script')[0])

		# Handling situation, when we couldn't parse page number from `script` HTML element 
		# In that case exit with status 1
		try:
			page_number = int(self.get_page_number(page_number_el))
		except PageNumberNotFoundError as e:
			print(f'Error: {e}')
			sys.exit(1)
		except Exception as e:
			print(f'Some Unexpected error occured: {e}')
			sys.exit(1)

		if actual_iteration_of_page != page_number:
			return []

		items_on_page = []
		items_el_parent = soup.find_all('div', {'class': 'group_discounts', 'data-page': f'{page_number}'})
		for item_el_parent in items_el_parent:
			item_el = item_el_parent.findChildren('div', {'class': 'log_product product_name wide'})[0]
			shops = self.scrape_shops_from_item(item_el_parent)
			# TODO price
			items_on_page.append({
				'name': item_el.h2.a.get('title'),
				'amount': item_el.h2.span.text.strip(),
				'endpoint': item_el.h2.a.get('href'),
				'data-product': item_el.h2.a.get('data-product'),
				'shops': shops,
				# 'price':
			})

		return items_on_page

	def scrape_shops_from_item(self, item_el):
		print(item_el.h2.a.get('title'))
		item_details_table = item_el.findChildren('table', {'class': 'wide discounts_table'})[0]
		item_details_rows = item_details_table.find_all('tr')
		shops = []
		for row in item_details_rows:
			shops.append(row.find('td', {'class': 'discounts_shop_info'}).span.a.span.text)

		return shops

	def scrape_all_items_by_subcategory(self, subcategory_endpoint, shop_endpoint=None):
		if shop_endpoint:
			shop = shop_endpoint.split('/')[-1]
			file_name = f'{subcategory_endpoint.split("/")[-1]}_items_in_{shop}'
			URL_ITEMS_BASE = f'{self.URL_BASE}{subcategory_endpoint}/{shop}'
		else:
			file_name = f'{subcategory_endpoint.split("/")[-1]}_items'
			URL_ITEMS_BASE = f'{self.URL_BASE}{subcategory_endpoint}'

		items_subcategory = []
		actual_iteration_of_page = 1
		while True:
			URL_ITEMS = URL_ITEMS_BASE + f'?page={actual_iteration_of_page}'

			items_html = self.get_html_from_url(URL_ITEMS)
			try:
				soup = BeautifulSoup(items_html, 'html.parser')
			except: 
				print(f'Couldn\'t scrape kupi.cz HTML to get items from subcategory {subcategory_endpoint.split("/")[-1]}')
				sys.exit(1)

			items_on_page = self.scrape_items_from_html(soup, actual_iteration_of_page)
			if not items_on_page:
				break

			items_subcategory.append(items_on_page)
			actual_iteration_of_page += 1

		if items_subcategory:
			write_item_to_json(file_name, items_subcategory)

		return items_subcategory

	def get_page_number(self, string):
		"""Parse page number from `script` HTML element."""
		pattern = r'var sent_page = \[(\d+)]'
		matches = re.findall(pattern, string)
		if matches:
			return matches[0]
		else:
			raise PageNumberNotFoundError('Couldn\'t parse page number from HTML.')


def main():
	kupi_scrapper = KupiScrapper()
	categories_dict = kupi_scrapper.scrape_categories()
	shops_dict = kupi_scrapper.scrape_shops()
	subcategories_dict = kupi_scrapper.scrape_subcategories(categories_dict)
	items_subcategory = kupi_scrapper.scrape_all_items_by_subcategory('/slevy/ovoce-a-zelenina')


if __name__ == '__main__':
	main()
