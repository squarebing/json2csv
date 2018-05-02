from collections import defaultdict
import csv
import json
import sys
import time
import re
import configparser
from distutils.util import strtobool


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
	print("Usage: csv2json.py <file.csv>")
	sys.exit(0)
elif len(sys.argv)==2:
	file = sys.argv[1]

csvData=[]
f = open(file, "r")

reader = csv.reader(f)
for row in reader:
	csvData.append(row)

fields = csvData[0]
	
try:
	parentIndex=fields.index(parentColumn)
	nodeIndex=fields.index(nodeColumn)
except:
	print("Cannot find parent column or the node column")
	sys.exit(0)
  
# contstruct list of parents
parents = defaultdict(list)
attributes = {}
attributeTypes = {}
for row in csvData:
	parents[row[parentIndex]].append(row)
	
	for field in fields:
		if row[fields.index(field)].find(subItemEscapeChar)== 0:
			if  row[fields.index(field)].find(subItemEscapeChar+"list"+subItemEscapeChar)> 0:
				attributeTypes[row[nodeIndex]] ="list"

			elif  row[fields.index(field)].find(subItemEscapeChar+"dict"+subItemEscapeChar)> 0:
				attributeTypes[row[nodeIndex]] ="dict"

			attributes[row[nodeIndex]]= row[fields.index(field)].replace(subItemEscapeChar+"list"+subItemEscapeChar,"")
			attributes[row[nodeIndex]]= attributes[row[nodeIndex]].replace(subItemEscapeChar+"dict"+subItemEscapeChar,"")
			attributes[row[nodeIndex]]= attributes[row[nodeIndex]].replace(subItemEscapeChar,"")


#print(parents)
#print(attributes)
#print(attributeTypes)

def buildtree(t=None, parent=''):
	
	#Get all the children rows for a given parent
	rows = parents.get(parent, None)
	
	attributesLabel=""
	attrType=""


	try:
		attributesLabel = attributes[parent]
		attrType = attributeTypes[parent]
	except:
		pass

	if rows is None:
		return t

		
	for row in rows:

		node = {}
		
		for field in fields:
			if row[fields.index(field)] !="": 
				if row[fields.index(field)].find(subItemEscapeChar)== 0:
					pass
				else:
					if row[fields.index(field)].find(simpleListEscapeChar)== 0:
						node[field]=json.loads(row[fields.index(field)].replace(simpleListEscapeChar,""))
					elif row[fields.index(field)].find(booleanEscapeChar)== 0:
						node[field]=bool(strtobool(row[fields.index(field)].replace(booleanEscapeChar,"")))
					else:
						node[field]=row[fields.index(field)]
		
		if t is None:
			t = node
		else:
			#print(attrType,len(rows) )
			if attributesLabel =="":
				print("there are sub elements that don't have a parent, this script will fail to generate the proper result")
			elif attrType =="dict" and len(rows) ==1:
				t[attributesLabel]= node
			else:
				children = t.setdefault(attributesLabel, []) 
				children.append(node)
			
			
		buildtree(node, node[nodeColumn])
	
	return t
	
data = buildtree()

def stripParentNode(data):
    if isinstance(data, dict):
        return {k:stripParentNode(v) for k, v in data.items() if k != nodeColumn and k != parentColumn}
    elif isinstance(data, list):
        return [stripParentNode(item) for item in data if item is not None]
    elif isinstance(data, tuple):
        return tuple(stripParentNode(item) for item in data if item is not None)
    elif isinstance(data, set):
        return {stripParentNode(item) for item in data if item is not None}
    else:
        return data
		
data = stripParentNode(data)

#j=json.loads(json.dumps(data))
#print( json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))

outrFile = file+'_'+ str(int(time.time()))+'.json'

def redirect_to_file(text, outrFile):
	original = sys.stdout
	sys.stdout = open(outrFile, 'w')
	print(text)
	sys.stdout = original
	
	
redirect_to_file(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')), outrFile)

