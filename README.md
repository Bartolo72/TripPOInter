# TripPOInter

TripPOInter is a Python library for generating and enriching Points of Interest (POIs) for trip planning. It uses various data sources to gather information about attractions, landmarks, and other interesting places in a city.

## Features

- Automatic POI discovery for any city
- Rich POI data including:
  - Basic information (name, location, address)
  - Ratings and reviews
  - Opening hours
  - Contact information
  - Categories and types
  - Price levels
- Extensible fetcher system for adding new data sources
- Flexible metadata system for storing additional information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TripPOInter.git
cd TripPOInter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# For Google Maps API
export GOOGLE_MAPS_API_KEY="your_api_key_here"
export GOOGLE_MAPS_RADIUS="1000"  # Optional, default is 1000 meters
```

## Usage

Basic usage example:

```python
from datetime import datetime
from trippointer import TripPOInter

# Create a TripPOInter instance
trippointer = TripPOInter(
    city_name="Paris",
    country_name="France",
    start_date=datetime(2024, 4, 1),
    end_date=datetime(2024, 4, 5)
)

# Fetch POIs (this happens automatically during initialization)
# The GoogleMapsFetcher will generate initial POIs

# Enrich POIs with additional data
trippointer.fetch()

# Get all POIs
pois = trippointer.get_pois()

# Access POI data
for poi in pois:
    print(f"Name: {poi.name}")
    print(f"Address: {poi.address}")
    print(f"Rating: {poi.rating}")
    
    # Access Google Maps metadata
    if "google_maps" in poi.metadata:
        google_data = poi.metadata["google_maps"]
        print(f"Total ratings: {google_data['user_ratings_total']}")
        print(f"Opening hours: {google_data['opening_hours']}")

# Save POIs to a file
trippointer.save()
```

## Project Structure

```
trippointer/
├── __init__.py
├── core.py              # Main TripPOInter class
├── models.py            # Data models (POI, TripPoint)
└── fetchers/
    ├── __init__.py     # Base fetcher class and discovery
    └── google_maps_fetcher.py  # Google Maps implementation
```

## Creating Custom Fetchers

You can create custom fetchers by inheriting from `TripPOFetcher`:

```python
from trippointer.fetchers import TripPOFetcher

class MyCustomFetcher(TripPOFetcher):
    name = "my_custom_fetcher"
    is_base_fetcher = False  # Set to True if this fetcher generates initial POIs

    def fetch(self, poi=None):
        if poi is None:
            # Generate initial POIs
            return {"pois": [...]}
        else:
            # Enrich existing POI
            return {"additional_data": "..."}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
