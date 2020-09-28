import json

### region JSON

def write_item_to_json(file_name, items):
	"""Write dictionary with item details into JSON file."""

	try:
		with open(f'./json/{file_name}.json', 'w') as file:
			for item_list in items:
				for item in item_list:
					json.dump(item, file, indent=4)
					file.write(',\n')
		print('All items were successfully written into JSON object.')
	except Exception as e:
		print(f'Couldn\'t write items into JSON object. Error: {e}')

### endregion JSON

### region REDIS

def get_dict_from_redis(client, pattern):
	"""
		Get each component (categories / shops) from Redis DB
	"""

	kupi_components_redis = client.keys(pattern=pattern)
	if not kupi_components_redis:
		return {}
	else:
		kupi_components_dict = {}
		for component_key in kupi_components_redis:
			component_values = client.hgetall(component_key)
			name = component_values['name']
			endpoint = component_values['endpoint']
			kupi_components_dict[name] = endpoint

		return kupi_components_dict

def store_types_into_redis(client, kupi_components_dict, kupi_group):
	"""
		Store every component (categories / shops) into Redis DB
	"""

	it = 1
	for name_deserialized, endpoint in kupi_components_dict.items():
		name_serialized = endpoint.split("/")[-1]
		serialized_type_key = 'data_category' if kupi_group == 'categories' else 'data_shop'
		client.hset(f'{kupi_group}:{name_serialized}', mapping={'ID': it,
																'name': name_deserialized,
																f'{serialized_type_key}': name_serialized,
																'endpoint': endpoint})
		it += 1

def store_subcategories_into_redis(client, subcategories_from_all_categories_dict, category_name):
	""" 
		Go through every single subcategory from every category available on `kupi.cz`
		Store informations about subcategories into Redis DB 
	"""

	it = 1
	subcategories_from_one_category_dict = {}
	for key, value in subcategories_from_all_categories_dict.items():
		print(f'Key name: {key}')
		for subcat in value:
			name_deserialized = subcat['name']
			name_serialized = subcat['data-category']
			endpoint = subcat['endpoint']
			client.hset(f'subcategories:{key}:{name_serialized}', mapping={'ID': it,
																		   'name': name_deserialized,
																		   'data_category': name_serialized,
																		   'endpoint': endpoint,
																		   'category': key})

			# If we are currently iterating over subcategories from desired category, store its `name` and `endpoint
			# into dictionary
			if key == category_name:
				subcategories_from_one_category_dict[name_deserialized] = endpoint

		it += 1

	return subcategories_from_one_category_dict

### endregion REDIS
