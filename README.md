# JSON to Excel
This app flattens a json file and exports to Excel

For example, if you were to start with a nested JSON object like this:

```
{
  "name": "John",
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA"
  },
  "phones": [
    {
      "type": "home",
      "number": "123-456-7890"
    },
    {
      "type": "work",
      "number": "987-654-3210"
    }
  ],
  "email": "john.doe@example.com"
}
```
it would be flattened into something like this:

```
{
  "name": "John",
  "address_street": "123 Main St",
  "address_city": "Anytown",
  "address_state": "CA",
  "phones_0_type": "home",
  "phones_0_number": "123-456-7890",
  "phones_1_type": "work",
  "phones_1_number": "987-654-3210",
  "email": "john.doe@example.com"
}
```
