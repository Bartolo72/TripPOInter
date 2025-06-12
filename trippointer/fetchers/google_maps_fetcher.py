import os
from typing import Any, Optional, List

import googlemaps
from datetime import datetime

from ..models import POI
from . import TripPOFetcher


class GoogleMapsFetcher(TripPOFetcher):
    name = "google_maps"
    is_base_fetcher = True

    def __init__(self, trippointer: Any) -> None:
        super().__init__(trippointer)
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.radius: int = int(os.getenv("GOOGLE_MAPS_RADIUS", "1000"))
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable is required")
        self.client = googlemaps.Client(key=self.api_key)

    def fetch(self, poi: Optional[POI] = None) -> dict[str, Any]:
        """Fetch POIs or enrich an existing POI.

        If poi is None, generates initial list of POIs for the city.
        If poi is provided, enriches it with additional data.
        """
        if poi is None:
            return self._generate_pois()
        return self._enrich_poi(poi)

    def _generate_pois(self) -> dict[str, Any]:
        """Generate initial list of POIs for the city."""
        try:
            geocode_result = self.client.geocode(
                f"{self.city_name}, {self.country_name}"
            )
            if not geocode_result:
                return {"pois": []}

            location = geocode_result[0]["geometry"]["location"]

            places_result = self.client.places_nearby(
                location=(location["lat"], location["lng"]),
                radius=self.radius,
                type="tourist_attraction",
            )

            pois = []
            for place in places_result.get("results", []):
                place_details = self.client.place(
                    place["place_id"],
                    fields=[
                        "name",
                        "formatted_address",
                        "geometry/location",
                        "rating",
                        "user_ratings_total",
                        "opening_hours",
                        "website",
                        "formatted_phone_number",
                        "type",
                        "price_level",
                        "review",
                    ],
                )["result"]

                poi = POI(
                    name=place_details.get("name", "Unknown"),
                    description=None,
                    latitude=place_details["geometry"]["location"]["lat"],
                    longitude=place_details["geometry"]["location"]["lng"],
                    address=place_details.get("formatted_address"),
                    category=place_details.get("type", ""),
                    rating=place_details.get("rating"),
                    opening_hours=place_details.get("opening_hours", {}).get(
                        "weekday_text", []
                    ),
                    website=place_details.get("website"),
                    phone=place_details.get("formatted_phone_number"),
                    source="Google Maps",
                )
                pois.append(poi)

            return {"pois": pois}

        except Exception as e:
            print(f"Error generating POIs for {self.city_name}: {e}")
            return {"pois": []}

    def _enrich_poi(self, poi: POI) -> dict[str, Any]:
        """Enrich an existing POI with additional data."""
        try:
            places_result = self.client.places(
                query=poi.name,
                location=(poi.latitude, poi.longitude),
                radius=self.radius,
            )

            if not places_result.get("results"):
                return {}

            place = places_result["results"][0]
            place_id = place["place_id"]

            place_details = self.client.place(
                place_id,
                fields=[
                    "name",
                    "formatted_address",
                    "geometry/location",
                    "rating",
                    "user_ratings_total",
                    "opening_hours",
                    "website",
                    "formatted_phone_number",
                    "type",
                    "price_level",
                    "review",
                ],
            )["result"]

            return {
                "google_place_id": place_id,
                "formatted_address": place_details.get("formatted_address"),
                "rating": place_details.get("rating"),
                "user_ratings_total": place_details.get("user_ratings_total"),
                "opening_hours": place_details.get("opening_hours", {}).get(
                    "weekday_text", []
                ),
                "website": place_details.get("website"),
                "formatted_phone": place_details.get("formatted_phone_number"),
                "type": place_details.get("type"),
                "price_level": place_details.get("price_level"),
                "reviews": place_details.get("review", []),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            print(f"Error enriching POI {poi.name}: {e}")
            return {}
