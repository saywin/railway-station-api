from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


from station.models import OrderModel, TicketModel
from station.serializers import OrderListSerializer, OrderSerializer
from station.tests.tests_api.test_helpers import create_journey

URL_ORDER_LIST = reverse("station:order-list")


def create_ticket(order: OrderModel, **kwargs):
    journey = create_journey()
    data = {"cargo": 10, "seat": 15, "journey": journey, "order": order}
    data.update(**kwargs)
    return TicketModel.objects.create(**data)


class UnAuthorizedJourneyTest(APITestCase):
    def test_station_list_unauthorized(self):
        res = self.client.get(URL_ORDER_LIST)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedJourneyTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )
        self.order_1 = OrderModel.objects.create(user=self.user)
        create_ticket(order=self.order_1)
        self.client.force_authenticate(self.user)

    def test_create_order_with_tickets(self):
        journey = create_journey()
        tickets = [
            {"cargo": 1, "seat": 10, "journey": journey.id},
            {"cargo": 1, "seat": 11, "journey": journey.id},
        ]
        res = self.client.post(URL_ORDER_LIST, {"tickets": tickets}, format="json")
        order = OrderModel.objects.get(id=res.data["id"])
        serializer = OrderSerializer(order)
        print(serializer.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, res.data)

    def test_create_order_without_tickets(self):
        res = self.client.post(URL_ORDER_LIST, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list(self):
        res = self.client.get(URL_ORDER_LIST)
        orders = OrderModel.objects.all()
        serializer = OrderListSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(orders.count(), 1)
        self.assertIn(serializer.data[0], res.data["results"])

    def test_order_with_invalid_seat_cargo(self):
        journey = create_journey()
        ticket_1 = [
            {"cargo": 33, "seat": 15, "journey": journey.id},
        ]
        res_1 = self.client.post(URL_ORDER_LIST, {"tickets": ticket_1}, format="json")
        ticket_2 = [
            {"cargo": 10, "seat": 33, "journey": journey.id},
        ]
        res_2 = self.client.post(URL_ORDER_LIST, {"tickets": ticket_2}, format="json")
        self.assertEqual(res_1.status_code, 400)
        self.assertEqual(res_2.status_code, 400)

    def test_order_del_forbidden(self):
        url = reverse("station:order-detail", args=[self.order_1.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
