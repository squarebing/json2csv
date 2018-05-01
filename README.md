# json2csv and csv2json

These two python scripts onvert files between JSON and CSV. They are tested with Python 3.6.5

## Requirements

- The JSON structure can have nested attributes. However, every array element in the json MUST have an attribute.
- Please make sure the JSON file doesn't contain any special atttributes, as defined in config.ini

## Usage

```sh
python json2csv.py <JSON file>
python csv2json.py <CSV file>
```

## Json that works

```json
{
    "id": "User:1.0",
    "name": "User",
    "description": "User Account",
    "attributes": [
        {
            "name": "id",
            "type": "string"
        },
        {
            "name": "name",
            "type": "complex",
            "multiValued": false,
            "description": "The components of the user's real name",
            "required": false,
            "dataClassification": "personal",
            "subAttributes": [
                {
                    "name": "firstName",
                    "type": "string",
                    "multiValued": false
                },
                {
                    "name": "lastName",
                    "type": "string",
                    "multiValued": true
                }
            ]
        }
    ]
}
```

## Json that doesn't work

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