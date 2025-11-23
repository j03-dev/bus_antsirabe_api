# Bus Antsirabe API

A simple REST API for retrieving bus line and travel information for Antsirabe.

## Endpoints

### GET /api/v1/travels

Returns a list of all available travels with their IDs and names.

Response format:
```json
{
  "travel_id": "travel_name"
}
```

### POST /api/v1/travels

Find bus lines between two points.

Request body:
```json
{
  "primus": "starting_point_id",
  "terminus": "destination_id"
}
```

Response format:
```json
["bus_line_1", "bus_line_2"]
```

## Running locally

1. Clone the repository
2. Install dependencies: `pip install .`
3. Run the server: `python src/main.py`
4. API will be available at http://localhost:8080

## Data

Bus line data is stored in `data/travel.json` and loaded on startup.
