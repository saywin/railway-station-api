from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from station.models import RouteModel
from station.serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
)
from station.tests.tests_api.test_helpers import create_station, create_route

URL_ROUTE_LIST = reverse("station:route-list")


def detail_route_url(pk: int) -> str:
    return reverse("station:route-detail", args=[pk])


class UnAuthorizedRouteTest(APITestCase):
    def test_route_list_unauthorized(self):
        res = self.client.get(URL_ROUTE_LIST)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedCrewTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )
        self.client.force_authenticate(user)

    def test_route_list(self):
        source_route_2 = create_station(name="Poltava")
        create_route()
        create_route(source=source_route_2)
        res = self.client.get(URL_ROUTE_LIST)
        routes = RouteModel.objects.all()
        serializer = RouteListSerializer(routes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(routes.count(), 2)
        self.assertIn(serializer.data[0], res.data["results"])
        self.assertIn(serializer.data[1], res.data["results"])

    def test_route_detail(self):
        route = create_route()
        url = detail_route_url(route.id)
        res = self.client.get(url)
        serializer = RouteDetailSerializer(route)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_route_create_forbidden(self):
        source = create_station()
        destination = create_station(name="Lviv")
        payload = {
            "source": source,
            "destination": destination,
            "distance": 500,
        }
        res = self.client.post(URL_ROUTE_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_filter_by_source_and_destination(self):
        source = create_station(name="Lisichansk")
        destination = create_station(name="Lviv")
        route_1 = create_route(source=source, destination=destination)
        route_2 = create_route(source=source)
        route_3 = create_route(destination=destination)
        serializer_route_1 = RouteListSerializer(route_1)
        serializer_route_2 = RouteListSerializer(route_2)
        serializer_route_3 = RouteListSerializer(route_3)

        res_source = self.client.get(URL_ROUTE_LIST, {"source": "Lisichansk"})
        self.assertEqual(res_source.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_route_1.data, res_source.data["results"])
        self.assertIn(serializer_route_2.data, res_source.data["results"])
        self.assertNotIn(serializer_route_3.data, res_source.data["results"])

        res_destination = self.client.get(
            URL_ROUTE_LIST,
            {"destination": "Lviv"}
        )
        self.assertEqual(res_destination.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_route_1.data, res_destination.data["results"])
        self.assertIn(serializer_route_3.data, res_destination.data["results"])
        self.assertNotIn(
            serializer_route_2.data,
            res_destination.data["results"]
        )


class AdminRouteTest(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(admin)

    def test_route_list(self):
        res = self.client.get(URL_ROUTE_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_route_create(self):
        source = create_station()
        destination = create_station(name="Lviv")
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 500,
        }
        res = self.client.post(URL_ROUTE_LIST, payload)
        route = RouteModel.objects.get(pk=res.data["id"])
        serializer = RouteSerializer(route)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["source"], payload["source"])
        self.assertEqual(res.data["destination"], payload["destination"])
        self.assertEqual(res.data["distance"], payload["distance"])
        self.assertEqual(res.data, serializer.data)

    def test_route_del_forbidden(self):
        route = create_route()
        res = self.client.delete(detail_route_url(route.id))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
