from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from station.models import TrainTypeModel
from station.serializers import TrainTypeSerializer

URL_TRAIN_TYPE_LIST = reverse("station:train_type-list")


def create_train_type():
    return TrainTypeModel.objects.create(name="Heavy Rail")


class UnAuthorizationTrainTypeTest(APITestCase):
    def test_train_type_get_no_access(self):
        res = self.client.get(URL_TRAIN_TYPE_LIST)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizationTrainTypeTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )
        self.client.force_authenticate(user)

    def test_train_type_create_forbidden(self):
        res = self.client.post(URL_TRAIN_TYPE_LIST, {"name": "Light Rail"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_train_type_list(self):
        train_type = create_train_type()
        res = self.client.get(URL_TRAIN_TYPE_LIST)
        serializer = TrainTypeSerializer(train_type)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, res.data["results"])
        self.assertEqual(res.data["count"], 1)

    def test_train_type_detail(self):
        train_type = create_train_type()
        url = reverse("station:train_type-detail", args=[train_type.id])
        res = self.client.get(url)

        serializer = TrainTypeSerializer(train_type)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminTrainTypeTest(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_user(
            email="admin@admin.com", password="password", is_staff=True
        )
        self.client.force_authenticate(admin)

    def test_train_type_create(self):
        res = self.client.post(URL_TRAIN_TYPE_LIST, {"name": "Light Rail"})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "Light Rail")

    def test_train_type_del_forbidden(self):
        train_type = create_train_type()
        url = reverse("station:train_type-detail", args=[train_type.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
