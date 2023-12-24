# Bus Antsirabe api

## List all bus stop

- end-point: `/api/travel`
- method: `get`
- response:

```json
{
  "1": "4chemin ambalavato",
  "10": "ampahatra",
  "11": "ampihaviana",
  "12": "andrangy",
  "13": "andranomadio",
  "14": "andranomafana",
  "15": "andranonahoatra",
  "16": "antanimena",
  "17": "antanivao"
  //
}
```

## List of buses to take

- end-point: `/api/travel`
- method: `post`
- body:

```json
{
  "a": {
    "id": 8,
    "name": "ambohimena"
  },
  "b": {
    "id": 77,
    "name": "zaodahy"
  }
}
```
- response
```json
[
  "BUS 4",
  "BUS 10",
  "BUS 12",
  "BUS 16",
  "BUS 17",
  "BUS 19"
]
```
