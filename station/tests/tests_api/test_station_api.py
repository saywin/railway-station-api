from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from station.models import StationModel
from station.serializers import StationSerializer
from station.tests.tests_api.test_helpers import create_station

URL_STATION_LIST = reverse("station:station-list")


def detail_station_url(pk: int) -> str:
    return reverse("station:station-detail", args=[pk])


class UnAuthorizedStationTest(APITestCase):
    def test_station_list_unauthorized(self):
        res = self.client.get(URL_STATION_LIST)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedStationTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )
        self.client.force_authenticate(user)

    def test_station_list(self):
        create_station()
        create_station(name="Kyiv Passage")
        res = self.client.get(URL_STATION_LIST)
        station = StationModel.objects.all()
        serializer = StationSerializer(station, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(station.count(), 2)
        self.assertEqual(serializer.data, res.data["results"])

    def test_crew_detail(self):
        station = create_station()
        url = detail_station_url(station.id)
        res = self.client.get(url)
        serializer = StationSerializer(station)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_train_create_forbidden(self):
        payload = {
            "first_name": "Test first name",
            "last_name": "Test last name",
        }
        res = self.client.post(URL_STATION_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainTest(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(admin)

    def test_station_list(self):
        res = self.client.get(URL_STATION_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_station_create(self):
        payload = {
            "name": "Test station",
            "latitude": 34.654654,
            "longitude": 56.75675,
        }
        res = self.client.post(URL_STATION_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["latitude"], payload["latitude"])
        self.assertEqual(res.data["longitude"], payload["longitude"])

    def test_station_del_forbidden(self):
        station = create_station()
        res = self.client.delete(detail_station_url(station.id))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
