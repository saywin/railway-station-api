from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from station.models import TrainTypeModel, TrainModel
from station.serializers import TrainListSerializer, TrainDetailSerializer

URL_TRAIN_LIST = reverse("station:train-list")


def detail_train_url(pk: int) -> str:
    return reverse("station:train-detail", args=[pk])


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


class UnAuthorizedTrainTest(APITestCase):
    def test_train_get_unauthorized(self):
        res = self.client.get(URL_TRAIN_LIST)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedTrainTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )
        self.client.force_authenticate(user)

    def test_train_list(self):
        create_train()
        create_train(name="Dnipro train")
        res = self.client.get(URL_TRAIN_LIST)
        trains = TrainModel.objects.all()
        serializer = TrainListSerializer(trains, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(trains.count(), 2)
        self.assertEqual(serializer.data, res.data["results"])

    def test_train_detail(self):
        train = create_train()
        url = detail_train_url(train.id)
        res = self.client.get(url)
        serializer = TrainDetailSerializer(train)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_train_create_forbidden(self):
        train_type = TrainTypeModel.objects.create(name="Heavy Rail")
        payload = {
            "name": "Test",
            "cargo_num": 2,
            "places_in_cargo": 3,
            "train_type": train_type,
        }

        res = self.client.post(URL_TRAIN_LIST, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainTest(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(admin)

    def test_train_list(self):
        res = self.client.get(URL_TRAIN_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_train_create(self):
        train_type = TrainTypeModel.objects.create(name="test")
        payload = {
            "name": "Test train",
            "cargo_num": 20,
            "places_in_cargo": 10,
            "train_type": train_type.id,
        }
        res = self.client.post(URL_TRAIN_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["train_type"], train_type.id)

    def test_train_del_forbidden(self):
        train = create_train()
        res = self.client.delete(detail_train_url(train.id))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
