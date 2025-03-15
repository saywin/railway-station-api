from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from station.models import (
    TrainTypeModel,
    TrainModel,
    CrewModel,
    StationModel,
    RouteModel,
    JourneyModel,
    OrderModel,
    TicketModel,
)


def create_user(**kwargs):
    payload = {"email": "user@user.com", "password": "1qazcde3"}
    payload.update(**kwargs)
    return get_user_model().objects.create_user(**payload)


def create_station(**kwargs):
    payload = {
        "name": "Kyiv-Passenger",
        "latitude": 50.4396935,
        "longitude": 30.4881173,
    }
    payload.update(**kwargs)
    return StationModel.objects.create(**payload)


def create_route(**kwargs):
    station_1 = create_station()
    station_2 = create_station(name="Dnipro-Main")
    payload = {"source": station_1, "destination": station_2, "distance": 532}
    payload.update(**kwargs)
    return RouteModel.objects.create(**payload)


def create_crew(**kwargs):
    payload = {
        "first_name": "Test",
        "last_name": "Testovich",
    }
    payload.update(**kwargs)
    return CrewModel.objects.create(**payload)


def create_train_type(**kwargs):
    payload = {"name": "Light Rail"}
    payload.update(**kwargs)
    return TrainTypeModel.objects.create(**payload)


def create_train(**kwargs):
    train_type = create_train_type()
    payload = {
        "name": "Test train",
        "cargo_num": 20,
        "places_in_cargo": 30,
        "train_type": train_type,
    }
    payload.update(**kwargs)
    return TrainModel.objects.create(**payload)


def create_journey(**kwargs):
    route = create_route()
    train = create_train()
    crew = create_crew()
    payload = {
        "route": route,
        "train": train,
        "departure_time": "2022-12-31 20:33",
        "arrival_time": "2022-12-31 22:40",
    }
    payload.update(**kwargs)
    journey = JourneyModel.objects.create(**payload)
    journey.crews.add(crew)
    return journey


class TrainTypeModelTest(TestCase):
    def setUp(self):
        self.train_type = create_train_type()

    def test_create_train_type(self):
        train_type_2 = TrainTypeModel.objects.create(name="Heavy Rail")
        self.assertEqual(TrainTypeModel.objects.count(), 2)
        self.assertIn(self.train_type, TrainTypeModel.objects.all())
        self.assertIn(train_type_2, TrainTypeModel.objects.all())

    def test_train_type_str(self):
        self.assertEqual(str(self.train_type), self.train_type.name)

    def test_db_table_name(self):
        self.assertEqual(TrainTypeModel._meta.db_table, "train_type")


class TrainModelTest(TestCase):
    def setUp(self):
        self.train = create_train()

    def test_create_train_type(self):
        self.assertEqual(TrainTypeModel.objects.count(), 1)
        self.assertIn(self.train, TrainModel.objects.all())

    def test_train_str(self):
        self.assertEqual(str(self.train), self.train.name)

    def test_train_db_table_name(self):
        self.assertEqual(TrainModel._meta.db_table, "train")


class CrewModelTest(TestCase):
    def setUp(self):
        self.crew = create_crew()

    def test_crew_create(self):
        self.assertEqual(self.crew.first_name, "Test")
        self.assertEqual(self.crew.last_name, "Testovich")
        self.assertEqual(CrewModel.objects.count(), 1)

    def test_crew_full_name(self):
        self.assertEqual(
            self.crew.full_name, f"{self.crew.first_name} {self.crew.last_name}"
        )

    def test_crew_str(self):
        self.assertEqual(str(self.crew), self.crew.full_name)

    def test_crew_db_table_name(self):
        self.assertEqual(CrewModel._meta.db_table, "crew")


class StationModelTest(TestCase):
    def setUp(self):
        self.station = StationModel.objects.create(
            name="Kyiv-Passenger",
            latitude=50.4396935,
            longitude=30.4881173,
        )

    def test_station_create(self):
        self.assertEqual(self.station.name, "Kyiv-Passenger")
        self.assertEqual(StationModel.objects.count(), 1)
        self.assertIn(self.station, StationModel.objects.all())

    def test_station_str(self):
        self.assertEqual(str(self.station), self.station.name)

    def test_station_db_table_name(self):
        self.assertEqual(StationModel._meta.db_table, "station")


class RouteModelTest(TestCase):
    def setUp(self):
        self.station_1 = create_station()
        self.station_2 = create_station(
            name="Dnipro-Main",
            latitude=48.4500000,
            longitude=34.9833300,
        )
        self.route = RouteModel.objects.create(
            source=self.station_1, destination=self.station_2, distance=532
        )

    def test_route_create(self):
        self.assertEqual(RouteModel.objects.count(), 1)
        self.assertEqual(self.route.source, self.station_1)
        self.assertEqual(self.route.destination, self.station_2)
        self.assertEqual(self.route.distance, 532)
        self.assertIn(self.route, RouteModel.objects.all())

    def test_route_str(self):
        self.assertEqual(
            str(self.route),
            f"Source: {self.route.source.name}, destination: {self.route.destination.name}",
        )

    def test_route_db_table_name(self):
        self.assertEqual(RouteModel._meta.db_table, "route")


class JourneyModelTest(TestCase):
    def setUp(self):
        self.journey = create_journey()

    def test_journey_create(self):
        self.assertEqual(JourneyModel.objects.count(), 1)
        self.assertIn(self.journey, JourneyModel.objects.all())

    def test_journey_str(self):
        self.assertEqual(
            str(self.journey),
            f"{self.journey.route}, "
            f"departure: {self.journey.departure_time}, "
            f"arrival: {self.journey.arrival_time}",
        )

    def test_journey_db_table_name(self):
        self.assertEqual(JourneyModel._meta.db_table, "journey")


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.order = OrderModel.objects.create(user=self.user)

    def test_order_create(self):
        self.assertEqual(OrderModel.objects.count(), 1)
        self.assertIn(self.order, OrderModel.objects.all())
        self.assertEqual(self.order.user, self.user)

    def test_order_str(self):
        self.assertEqual(
            str(self.order), f"{self.order.user.email}, " f"{self.order.created_at}"
        )

    def test_order_db_table_name(self):
        self.assertEqual(OrderModel._meta.db_table, "order")


class TicketModelTest(TestCase):
    def setUp(self):
        user = create_user()
        self.order = OrderModel.objects.create(user=user)
        self.journey = create_journey()
        self.ticket = TicketModel.objects.create(
            cargo=2,
            seat=20,
            order=self.order,
            journey=self.journey,
        )

    def test_ticket_create_valid(self):
        self.assertEqual(TicketModel.objects.count(), 1)
        self.assertIn(self.ticket, TicketModel.objects.all())
        self.assertEqual(self.ticket.cargo, 2)
        self.assertEqual(self.ticket.seat, 20)

    def test_ticket_str(self):
        self.assertEqual(
            str(self.ticket),
            f"Order:{self.ticket.order.id}, "
            f"cargo: {self.ticket.cargo}, "
            f"seat: {self.ticket.seat}",
        )

    def test_ticket_create_invalid_cargo(self):

        with self.assertRaises(ValidationError):
            TicketModel.objects.create(
                order=self.order,
                journey=self.journey,
                cargo=30,
                seat=10,
            )
        with self.assertRaises(ValidationError):
            TicketModel.objects.create(
                order=self.order,
                journey=self.journey,
                cargo=0,
                seat=10,
            )

    def test_ticket_create_invalid_seat(self):
        with self.assertRaises(ValidationError):
            TicketModel.objects.create(
                order=self.order,
                journey=self.journey,
                cargo=2,
                seat=99,
            )
        with self.assertRaises(ValidationError):
            TicketModel.objects.create(
                order=self.order,
                journey=self.journey,
                cargo=2,
                seat=0,
            )

    def test_ticket_db_table_name(self):
        self.assertEqual(TicketModel._meta.db_table, "ticket")
