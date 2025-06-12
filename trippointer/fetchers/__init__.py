import importlib
import inspect
import os
from pathlib import Path
from typing import Type, Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core import TripPOInter
    from ..models import POI


class TripPOFetcher:
    name: str = "base_fetcher"
    is_base_fetcher: bool = False

    def __init__(self: "TripPOFetcher", trippointer: "TripPOInter") -> None:
        self.trippointer = trippointer
        self.city_name = trippointer.city_name
        self.country_name = trippointer.country_name
        self.start_date = trippointer.start_date
        self.end_date = trippointer.end_date
        self.output_file = trippointer.output_file

    def fetch(self, poi: Optional["POI"] = None) -> Dict[str, Any]:
        """Fetch additional information for a POI.

        Args:
            poi: The POI to fetch information for

        Returns:
            Dictionary containing additional information about the POI
        """
        raise NotImplementedError("Subclasses must implement fetch()")


def get_all_fetchers() -> list[Type[TripPOFetcher]]:
    """Discover and return all fetcher classes from the fetchers directory."""
    fetchers = []
    fetchers_dir = Path(__file__).parent

    for file in fetchers_dir.glob("*.py"):
        if file.name in ["__init__.py"]:
            continue

        module_name = file.stem
        module_path = f"{__package__}.{module_name}"

        try:
            module = importlib.import_module(module_path)

            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, TripPOFetcher)
                    and obj != TripPOFetcher
                ):
                    fetchers.append(obj)
        except Exception as e:
            print(f"Error loading fetcher from {module_name}: {e}")

    return fetchers
