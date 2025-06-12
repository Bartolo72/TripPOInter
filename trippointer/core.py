from datetime import datetime
from typing import Any, List
import json

from .fetchers import TripPOFetcher, get_all_fetchers
from .models import POI, TripPoint


class TripPOInter:
    def __init__(
        self: "TripPOInter",
        city_name: str,
        country_name: str,
        start_date: datetime,
        end_date: datetime,
        output_file: str,
    ) -> None:
        self.city_name: str = city_name
        self.country_name: str = country_name
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.output_file: str = (
            f"{city_name}_{country_name}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.jsonl"
        )
        self.data: dict[str, list[TripPoint]] = {"pois": []}
        self.fetchers: list[TripPOFetcher] = []

        # Automatically discover and initialize all fetchers
        for fetcher_class in get_all_fetchers():
            self.add_fetcher(fetcher_class(self))

    def get_pois(self: "TripPOInter") -> List[POI]:
        """Get all POIs from the data."""
        return self.data.get("pois", [])

    def add_fetcher(self: "TripPOInter", fetcher: TripPOFetcher) -> None:
        fetcher.trippointer = self
        self.fetchers.append(fetcher)

    def fetch(self: "TripPOInter") -> None:
        for poi in self.get_pois():
            for fetcher in self.fetchers:
                poi.metadata[fetcher.name] = fetcher.fetch(poi)

    def save(self: "TripPOInter") -> None:
        with open(self.output_file, "w") as f:
            for item in self.data:
                f.write(json.dumps(item) + "\n")
