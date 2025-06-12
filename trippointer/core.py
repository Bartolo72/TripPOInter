from datetime import datetime
from typing import Any, List, TYPE_CHECKING
import json

from .models import POI, TripPoint

if TYPE_CHECKING:
    from .fetchers import TripPOFetcher, get_all_fetchers


class TripPOInter:
    def __init__(
        self: "TripPOInter",
        city_name: str,
        country_name: str,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        self.city_name: str = city_name
        self.country_name: str = country_name
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.output_file: str = (
            f"{city_name}_{country_name}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.jsonl"
        )
        self.data: dict[str, Any] = {"pois": []}
        self.fetchers: list["TripPOFetcher"] = []

        from .fetchers import get_all_fetchers

        for fetcher_class in get_all_fetchers():
            self.add_fetcher(fetcher_class(self))

        # Run base fetchers and remove them
        base_fetchers = [f for f in self.fetchers if f.is_base_fetcher]
        for fetcher in base_fetchers:
            result = fetcher.fetch()
            if "pois" in result:
                self.data["pois"].extend(result["pois"])
            self.fetchers.remove(fetcher)

    def get_pois(self: "TripPOInter") -> List[POI]:
        """Get all POIs from the data."""
        return self.data.get("pois", [])

    def add_fetcher(self: "TripPOInter", fetcher: "TripPOFetcher") -> None:
        fetcher.trippointer = self
        self.fetchers.append(fetcher)

    def fetch(self: "TripPOInter") -> None:
        """Fetch POIs and enrich them with additional data."""
        # Then enrich existing POIs with additional data
        for poi in self.data["pois"]:
            for fetcher in self.fetchers:
                metadata = fetcher.fetch(poi)
                if metadata:
                    poi.metadata[fetcher.name] = metadata

    def save(self: "TripPOInter") -> None:
        with open(self.output_file, "w") as f:
            for poi in self.data.get("pois", []):
                f.write(json.dumps(poi) + "\n")
