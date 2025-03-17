from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from station.models import CrewModel
from station.serializers import CrewSerializer

URL_CREW_LIST = reverse("station:crew-list")


def create_crew(**kwargs) -> CrewModel:
    data = {
        "first_name": "Kyiv Pass",
        "last_name": 20,
    }
    data.update(**kwargs)
    return CrewModel.objects.create(**data)


def detail_crew_url(pk: int) -> str:
    return reverse("station:crew-detail", args=[pk])


class UnAuthorizedCrewTest(APITestCase):
    def test_crew_list_unauthorized(self):
        res = self.client.get(URL_CREW_LIST)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedCrewTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="user@user.com", password="password"
        )
        self.client.force_authenticate(user)

    def test_crew_list(self):
        create_crew()
        create_crew(last_name="Si")
        res = self.client.get(URL_CREW_LIST)
        crews = CrewModel.objects.all()
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(crews.count(), 2)
        self.assertEqual(serializer.data, res.data["results"])

    def test_crew_detail(self):
        crew = create_crew()
        url = detail_crew_url(crew.id)
        res = self.client.get(url)
        serializer = CrewSerializer(crew)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_train_create_forbidden(self):
        payload = {
            "first_name": "Test first name",
            "last_name": "Test last name",
        }
        res = self.client.post(URL_CREW_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainTest(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(admin)

    def test_crew_list(self):
        res = self.client.get(URL_CREW_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crew_create(self):
        payload = {
            "first_name": "Test first name",
            "last_name": "Test last name",
        }
        res = self.client.post(URL_CREW_LIST, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["first_name"], payload["first_name"])
        self.assertEqual(res.data["last_name"], payload["last_name"])

    def test_crew_del_forbidden(self):
        crew = create_crew()
        res = self.client.delete(detail_crew_url(crew.id))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
