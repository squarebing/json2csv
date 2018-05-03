# json2csv and csv2json

These two python scripts onvert files between JSON and CSV. They are tested with Python 3.6.5

## Requirements

- The JSON structure can have nested attributes.
- Each element can have different set of attributes.
- Json document with an array at the ROOT is also supported.
- Please make sure the JSON file doesn't contain any special atttributes that are also defined in config.ini

## Usage

First, please review the config.ini, and make sure your JSON doesn't contain columns or text in the config

To run the script:
```sh
python json2csv.py <JSON file>
python csv2json.py <CSV file>
```


## Sample Json Files

First, please review the config.ini, and make sure your JSON doesn't contain columns or text in the config

A simple JSON document:
```json
{
  "users": [
    {
      "id": "8773fe-ffff-42837498757",
      "externalId": "239482347928374",
      "userName": "mona@example.com",
      "name": {
        "givenName": "mona",
        "familyName": "octocat"
      },
      "active": true
    },
    {
      "id": "77563764-eb6-24-0598234-958243",
      "externalId": "sdfoiausdofiua",
      "userName": "hubot@example.com",
      "name": {
        "givenName": "hu",
        "familyName": "bot"
      },
      "active": false
    }
  ]
}
```

A JSON doc with Array at the ROOT:
```json
[
  {
    "id": "8773fe-ffff-42837498757",
    "externalId": "239482347928374",
    "userName": "mona@example.com",
    "name": {
      "givenName": "mona",
      "familyName": "octocat"
    },
    "active": true
  },
  {
    "id": "77563764-eb6-24-0598234-958243",
    "externalId": "sdfoiausdofiua",
    "userName": "hubot@example.com",
    "name": {
      "givenName": "hu",
      "familyName": "bot"
    },
    "active": false
  }
]
```


A complicated Json example:
```json
{
    "id": "User:1.0",
    "name": "User",
    "description": "User Account",
    "attributes": [
        {
            "name": "id",
            "type": "string",
            "description": "Unique identifier for the User - a uuid."
        },
        {
            "name": "name",
            "type": "complex",
            "description": "The components of the user's real name",
            "required": false,
            "subAttributes": [
                {
                    "name": "familyName",
                    "type": "string"
                },
                {
                    "name": "givenName",
                    "type": "string"
                },
                {
                    "name": "middleName",
                    "type": "string"
                }
            ]
        },
        {
            "name": "gender",
            "type": "string",
            "canonicalValues": [
                "Male",
                "Female"
            ]
        },
        {
            "name": "emails",
            "type": "complex",
            "multiValued": true,
            "description": "Email addresses for the user.",
            "required": false,
            "subAttributes": [
                {
                    "name": "value",
                    "type": "string",
                    "description": "Email addresses for the user."
                },
                {
                    "name": "type",
                    "type": "string",
                    "description": "A label indicating the attribute's function, e.g., 'work' or 'home'.",
                    "canonicalValues": [
                        "Business",
                        "Personal",
                        "Other"
                    ],
                    "mutability": "readWrite",
                    "returned": "default",
                    "uniqueness": "none"
                }
            ]
        },
        {
            "name": "phoneNumbers",
            "type": "complex",
            "multiValued": true,
            "description": "Phone numbers for the User. ",
            "required": false,
            "subAttributes": [
                {
                    "name": "value",
                    "type": "string",
                    "multiValued": false,
                    "description": "Phone number of the User."
                },
                {
                    "name": "type",
                    "type": "string",
                    "multiValued": false,
                    "description": "A label indicating the attribute's function, e.g., 'work', 'home', 'mobile'.",
                    "canonicalValues": [
                        "Work",
                        "Home",
                        "Cell",
                        "Fax",
                        "Pager",
                        "Other"
                    ]
                },
                {
                    "name": "primary",
                    "type": "boolean",
                    "description": "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred phone number or primary phone number.  The primary attribute value 'true' MUST appear no more than once.",
                    "required": false
                },
                {
                    "name": "countryCode",
                    "type": "string",
                    "multiValued": false,
                    "description": "A two-letter code defined in ISO 3166-1 alpha-2 denoting the country the phone number was issued in. e.g., US"
                },
                {
                    "name": "verified",
                    "type": "boolean",
                    "multiValued": false,
                    "description": "flag to note phone number has been verified by the user.",
                    "required": false
                }
            ]
        }
    ]
}

```
