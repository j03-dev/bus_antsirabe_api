# Bus Antsirabe api

## List all bus stop

### url ```https://bus-antsirabe.onrender.com/api/travel```


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
  "a": 8,
  "b":  77
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
