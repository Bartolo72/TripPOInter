from datetime import datetime

from trippointer import TripPOInter


if __name__ == "__main__":
    trippointer = TripPOInter(
        city_name="Paris",
        country_name="France",
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 1, 10),
    )

    trippointer.fetch()
    trippointer.save()
