import json

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
