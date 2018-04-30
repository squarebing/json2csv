# json2csv and csv2json
These two python scripts onvert files between JSON and CSV.
They are tested with Python 3.6.5


# Usage
```
python json2csv.py <JSON file>
python csv2json.py <CSV file>
```

# Requirement
 - Please make sure the JSON file doesn't contain any special atttributes, as defined in config.ini
 - Every array element in the json MUST have an attribute. Following JSON won't work.

```json
[
  {
    "name": "A green door"
  },
  {
    "name": "A red rose"
  }
]
```

