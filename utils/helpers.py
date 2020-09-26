import json, redis

### region JSON

def write_item_to_json(file_name, items):
	"""Write dictionary with item details into JSON file."""

	try:
		with open(f'../json/{file_name}.json', 'w') as file:
			for item_list in items:
				for item in item_list:
					json.dump(item, file, indent=4)
					file.write(',\n')
		print('All items were successfully written into JSON object.')
	except Exception as e:
		print(f'Couldn\'t write items into JSON object. Error: {e}')

### endregion JSON

### region REDIS

def get_types_dict_from_redis(client, kupi_group):
	kupi_components_dict = {}
	it = 1
	while True: 
		kupi_component = client.hgetall(f'{kupi_group}:{it}')
		if kupi_component:
			name = kupi_component['name']
			endpoint = kupi_component['endpoint']
			kupi_components_dict[name] = endpoint

			it += 1
		else:
			break

	return kupi_components_dict

def post_types_into_redis(client, kupi_components_dict, kupi_group):
	it = 1
	for name, endpoint in kupi_components_dict.items():
		client.hset(f'{kupi_group}:{it}', mapping={'ID': it, 'name': name, 'endpoint': endpoint})
		it += 1

### endregion REDIS
