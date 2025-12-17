# Bus Antsirabe API

A simple REST API for retrieving bus line and travel information for Antsirabe.

## Endpoints

### GET /api/v1/travels

Returns a list of all available travels with their IDs and names.

Response format:
```json
[
  {
      "id": 7,
      "name": "Ambohidrano"
  },
  {
      "id": 67,
      "name": "Talata"
  }
  ...
]
```

### POST /api/v1/travels

Find bus lines between two points.

Request body:
```json
{
  "primus": 74,
  "terminus": 2,
}
```


Response format:
```json
[
  {
    "id": 4,
    "name": "BUS 10",
    "primus": {
        "id": 42,
        "name": "Dale"
    },
    "termius": {
        "id": 24,
        "name": "Antsira"
    },
    "travel": [
      {
          "id": 42,
          "name": "Dale"
      },
      {
          "id": 74,
          "name": "Vatofotsy"
      },
      {
          "id": 65,
          "name": "Stationnement (Piste)"
      },
      ...
    ]
  }
]
```

## Running locally

1. Clone the repository
2. Install dependencies: `pip install .`
3. Run the server: `python src/main.py`
4. API will be available at http://localhost:8080

## Data

Bus line data is stored in `data/travel.json` and loaded on startup.
