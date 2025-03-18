from datetime import datetime

from pytz import timezone

from station.models import (
    StationModel,
    RouteModel,
    TrainTypeModel,
    TrainModel,
    JourneyModel,
    CrewModel,
)


def create_station(**kwargs) -> StationModel:
    data = {
        "name": "Dnipro Main",
        "latitude": 30.6546456,
        "longitude": 32.746357,
    }
    data.update(**kwargs)
    return StationModel.objects.create(**data)


def create_route(**kwargs) -> RouteModel:
    source = create_station()
    destination = create_station(name="Kyiv Passage")
    data = {
        "source": source,
        "destination": destination,
        "distance": 532,
    }
    data.update(**kwargs)
    return RouteModel.objects.create(**data)


def create_train(**kwargs):
    train_type = TrainTypeModel.objects.create(name="Light Rail")
    data = {
        "name": "Kyiv Pass",
        "cargo_num": 20,
        "places_in_cargo": 30,
        "train_type": train_type,
    }
    data.update(**kwargs)
    return TrainModel.objects.create(**data)


def create_crew(**kwargs) -> CrewModel:
    data = {
        "first_name": "Taras",
        "last_name": "Smith",
    }
    data.update(**kwargs)
    return CrewModel.objects.create(**data)


def create_journey(**kwargs):
    departure_time = datetime(
        2022, 6, 14, 15, 34,
        tzinfo=timezone("Europe/Kiev")
    )
    arrival_time = datetime(
        2022, 6, 14, 21, 40,
        tzinfo=timezone("Europe/Kiev")
    )
    data = {
        "route": create_route(),
        "train": create_train(),
        "departure_time": departure_time,
        "arrival_time": arrival_time,
    }
    data.update(**kwargs)
    return JourneyModel.objects.create(**data)
