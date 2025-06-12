import os
from datetime import datetime
from typing import Any, Optional

import requests

from ..models import POI, TripPoint
from . import TripPOFetcher
from ..utils.vars import OPENTRIPMAP_URL


class OpenTripMapPOIFetcher(TripPOFetcher):
    def __init__(self, trippointer: Any) -> None:
        super().__init__(trippointer)
        self.radius: int = os.getenv("OPENTRIPMAP_RADIUS") | 5000
        self.limit: int = os.getenv("OPENTRIPMAP_LIMIT") | 50
        self.duration_minutes: int = os.getenv("OPENTRIPMAP_DURATION_MINUTES") | 120
        self.poi_categories: list[str] = os.getenv("OPENTRIPMAP_POI_CATEGORIES") | [
            "tourist",
            "cultural",
            "religious",
            "natural",
            "adventure",
            "shopping",
            "food",
            "beverage",
            "accomodation",
        ]
        self.url: str = OPENTRIPMAP_URL
        self.api_key = os.getenv("OPENTRIPMAP_API_KEY")
        if not self.api_key:
            raise ValueError("OPENTRIPMAP_API_KEY environment variable is required")

    def fetch(self) -> None:
        pois = self._fetch_pois()

        if "pois" not in self.trippointer.data:
            self.trippointer.data["pois"] = []
        self.trippointer.data["pois"].extend(pois)

    def _fetch_pois(self) -> list[POI]:
        params = {
            "radius": self.radius,
            "limit": self.limit,
            "apikey": self.api_key,
            "format": "json",
        }

        # Get coordinates for the city
        coordinates = self._get_city_coordinates()
        if not coordinates:
            return []

        params["lon"] = coordinates["lon"]
        params["lat"] = coordinates["lat"]

        try:
            # Get list of POIs
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            poi_list = response.json()

            # Get details for each POI
            pois = []
            for poi_data in poi_list:
                poi_details = self._get_poi_details(poi_data["xid"])
                if poi_details:
                    pois.append(poi_details)

            return pois
        except requests.RequestException as e:
            print(f"Error fetching POIs: {e}")
            return []

    def _get_city_coordinates(self) -> Optional[dict[str, float]]:
        params = {
            "name": self.city_name,
            "country": self.country_name,
            "apikey": self.api_key,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            return {"lat": data["lat"], "lon": data["lon"]}
        except requests.RequestException as e:
            print(f"Error getting city coordinates: {e}")
            return None

    def _get_poi_details(self, xid: str) -> Optional[POI]:
        url = f"{OPENTRIPMAP_URL}/xid/{xid}"
        params = {"apikey": self.api_key}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return POI(
                name=data.get("name", "Unknown"),
                description=data.get("wikipedia_extracts", {}).get("text"),
                latitude=data.get("point", {}).get("lat"),
                longitude=data.get("point", {}).get("lon"),
                address=data.get("address", {}).get("road"),
                category=(
                    data.get("kinds", "").split(",")[0] if data.get("kinds") else None
                ),
                rating=data.get("rate"),
                opening_hours=data.get("otm:opening_hours"),
                website=data.get("url"),
                phone=data.get("phone"),
                source="OpenTripMap",
            )
        except requests.RequestException as e:
            print(f"Error getting POI details: {e}")
            return None
