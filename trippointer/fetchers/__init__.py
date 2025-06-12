import importlib
import inspect
import os
from pathlib import Path
from typing import Type

from ..core import TripPOInter


class TripPOFetcher:
    def __init__(self: "TripPOFetcher", trippointer: TripPOInter) -> None:
        self.trippointer = trippointer
        self.city_name = trippointer.city_name
        self.country_name = trippointer.country_name
        self.start_date = trippointer.start_date
        self.end_date = trippointer.end_date
        self.output_file = trippointer.output_file

    def fetch(self) -> None:
        raise NotImplementedError("Subclasses must implement fetch()")


def get_all_fetchers() -> list[Type[TripPOFetcher]]:
    """Discover and return all fetcher classes from the fetchers directory."""
    fetchers = []
    fetchers_dir = Path(__file__).parent

    # Get all .py files in the fetchers directory
    for file in fetchers_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue

        # Convert file path to module path
        module_name = file.stem
        module_path = f"{__package__}.{module_name}"

        try:
            # Import the module
            module = importlib.import_module(module_path)

            # Find all classes in the module that inherit from TripPOFetcher
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
