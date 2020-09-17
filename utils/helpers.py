import json

def write_item_to_json(item):
	"""
		Write dictionary with item details into items.json file
	"""
	with open('../json/items.json', 'a') as file:
		json.dump(item, file, indent=4)
		file.write(',\n')
