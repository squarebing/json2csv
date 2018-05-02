from collections import defaultdict
import csv
import json
import sys
import time
import pprint
import uuid
import configparser

try:
	config = configparser.ConfigParser()
	config.read('config.ini')

	parentColumn=config['DEFAULT']['parentColumn'] 
	nodeColumn=config['DEFAULT']['nodeColumn'] 
	subItemEscapeChar=config['DEFAULT']['subItemEscapeChar'] 
	simpleListEscapeChar=config['DEFAULT']['simpleListEscapeChar'] 
	booleanEscapeChar=config['DEFAULT']['booleanEscapeChar'] 
		
except:
	print("Cannot read config file")
	sys.exit(0)

if len(sys.argv)<2:
	print("Usage: josn2csv.py <file.json>")
	sys.exit(0)
elif len(sys.argv)==2:
	file = sys.argv[1]
	
csv_data=[]
keys= []
  
with open(file) as json_data:
	d = json.load(json_data)

def getKeys(data):
	global keys
	
	if type(data) == type(dict()):
		for key,value in data.items():
			if key not in keys:
				keys.append(key)
				
			getKeys(data[key])
	elif type(data) == type(list()):
		for item in data:
			getKeys(item)

def isListsimple(aList):
	ans = True
	for item in aList:
		if type(item) in (type(list()), type(tuple()), type(dict())):
			ans = False
	return ans

def traverse(data, parent, current):
	global csv_data
	global keys
	
	node = {}

	node[parentColumn]= parent
	node[nodeColumn]= current
	
	if type(data) == type(list()):
		for item in data:
			traverse(item, parent, uuid.uuid4())
	else:
		for key in keys:
			node[key]=''
			if key in data:
				if type(data[key]) != type(dict()) and type(data[key]) != type(list()) :
					if type(data[key]) == type(bool()):
						node[key]=booleanEscapeChar + str(data[key])+ booleanEscapeChar
					else:
						node[key]=data[key]
				elif type(data[key]) == type(list()):
					if isListsimple(data[key]):
						node[key] =simpleListEscapeChar+json.dumps(data[key])+simpleListEscapeChar
					else:
						node[key]= subItemEscapeChar+key+subItemEscapeChar+"list"+subItemEscapeChar
				elif type(data[key]) == type(dict()):
					node[key]= subItemEscapeChar+key+subItemEscapeChar+"dict"+subItemEscapeChar

						
		csv_data.append(node)
						
		for key in keys:
			try:
				if type(data[key]) == type(dict()):
					traverse(data[key], current, uuid.uuid4())		
				elif  type(data[key]) == type(list()):
					if not isListsimple(data[key]):  
						for item in data[key]:
							traverse(item, current, uuid.uuid4())
			except:
				pass		
				

getKeys(d)
#print(keys)
traverse(d, None, uuid.uuid4())

outFile = file +'_'+ str(int(time.time()))+'.csv'
write_header = True
item_keys = []

with open(outFile, 'w', newline='') as csv_file:
	writer = csv.writer(csv_file)
 
	for item in csv_data:
		item_values = []
		for key in item:
			if write_header:
			   item_keys.append(key)
 
			value = item.get(key, '')
			if isinstance(value, str):
				item_values.append(value)
			else:
				item_values.append(value)
 
		if write_header:
			writer.writerow(item_keys)
			write_header = False
 
		writer.writerow(item_values)



		   