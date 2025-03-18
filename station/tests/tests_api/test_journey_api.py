from datetime import datetime
from pytz import timezone

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from station.models import JourneyModel, CrewModel
from station.serializers import (
    JourneyListSerializer,
    JourneyDetailSerializer,
    JourneySerializer,
)
from station.tests.tests_api.test_helpers import (
    create_route,
    create_train,
    create_station,
)

URL_JOURNEY_LIST = reverse("station:journey-list")
ROUTE = create_route()
TRAIN = create_train()


def detail_route_url(pk: int) -> str:
    return reverse("station:journey-detail", args=[pk])


def create_crew(**kwargs) -> CrewModel:
    data = {
        "first_name": "Taras",
        "last_name": "Smith",
    }
    data.update(**kwargs)
    return CrewModel.objects.create(**data)


def create_journey(**kwargs):
    departure_time = datetime(2022, 6, 14, 15, 34, tzinfo=timezone("Europe/Kiev"))
    arrival_time = datetime(2022, 6, 14, 21, 40, tzinfo=timezone("Europe/Kiev"))
    data = {
        "route": ROUTE,
        "train": TRAIN,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
    }
    data.update(**kwargs)
    return JourneyModel.objects.create(**data)


class UnAuthorizedCrewTest(APITestCase):
    def test_crew_list_unauthorized(self):
        res = self.client.get(URL_JOURNEY_LIST)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedCrewTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )

        self.station = create_station(name="Lviv station")
        route_2 = create_route(destination=self.station)
        route_3 = create_route(source=self.station)
        departure_time = datetime(2022, 4, 14, 12, 34, tzinfo=timezone("Europe/Kiev"))
        self.journey = create_journey()
        self.journey_2 = create_journey(route=route_2)
        self.journey_3 = create_journey(route=route_3, departure_time=departure_time)
        self.serializer_1 = JourneyListSerializer(self.journey)
        self.serializer_2 = JourneyListSerializer(self.journey_2)
        self.serializer_3 = JourneyListSerializer(self.journey_3)

        self.client.force_authenticate(user)

    def test_journey_list(self):
        res = self.client.get(URL_JOURNEY_LIST)
        routes = JourneyModel.objects.all()
        serializer = JourneyListSerializer(routes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(routes.count(), 2)
        self.assertIn(serializer.data[0], res.data["results"])
        self.assertIn(serializer.data[1], res.data["results"])

    def test_journey_detail(self):
        url = detail_route_url(self.journey.id)
        res = self.client.get(url)
        serializer = JourneyDetailSerializer(self.journey)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)
        print(JourneyDetailSerializer(self.journey).data)
        self.assertEqual(res.data, serializer.data)

    def test_journey_filter_by_source(self):
        res_filter_from = self.client.get(URL_JOURNEY_LIST, {"from": "dni"})
        self.assertEqual(res_filter_from.status_code, status.HTTP_200_OK)
        self.assertIn(self.serializer_1.data, res_filter_from.data["results"])
        self.assertIn(self.serializer_2.data, res_filter_from.data["results"])
        self.assertNotIn(self.serializer_3.data, res_filter_from.data["results"])

    def test_journey_filter_by_destination(self):
        res_filter_to = self.client.get(URL_JOURNEY_LIST, {"to": "Ky"})
        self.assertEqual(res_filter_to.status_code, status.HTTP_200_OK)
        self.assertIn(self.serializer_1.data, res_filter_to.data["results"])
        self.assertIn(self.serializer_3.data, res_filter_to.data["results"])
        self.assertNotIn(self.serializer_2.data, res_filter_to.data["results"])

    def test_journey_filter_by_date(self):
        res_filter_date = self.client.get(URL_JOURNEY_LIST, {"date": "2022-04-14"})
        self.assertEqual(res_filter_date.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.serializer_1.data, res_filter_date.data["results"])
        self.assertNotIn(self.serializer_2.data, res_filter_date.data["results"])
        self.assertIn(self.serializer_3.data, res_filter_date.data["results"])

    def test_journey_create_forbidden(self):
        departure_time = datetime(2023, 6, 14, 15, 34, tzinfo=timezone("Europe/Kiev"))
        arrival_time = datetime(2023, 6, 14, 21, 40, tzinfo=timezone("Europe/Kiev"))
        payload = {
            "route": ROUTE,
            "train": TRAIN,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
        }
        res = self.client.post(URL_JOURNEY_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminJourneyTest(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(admin)

    def test_journey_list(self):
        res = self.client.get(URL_JOURNEY_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_journey_create(self):
        departure_time = datetime(2020, 6, 14, 15, 34, tzinfo=timezone("Europe/Kiev"))
        arrival_time = datetime(2020, 6, 15, 21, 40, tzinfo=timezone("Europe/Kiev"))
        crew = create_crew()
        route = create_route()
        train = create_train()
        payload = {
            "route": route.id,
            "train": train.id,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "crews": crew.pk,
        }

        res = self.client.post(URL_JOURNEY_LIST, payload)
        print(payload["route"])
        print(res.json())
        journey = JourneyModel.objects.get(pk=res.data["id"])
        serializer = JourneySerializer(journey)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["route"], payload["route"])
        self.assertEqual(res.data["train"], payload["train"])
        self.assertEqual(res.data, serializer.data)

    def test_journey_del_forbidden(self):
        journey = create_route()
        res = self.client.delete(detail_route_url(journey.id))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
