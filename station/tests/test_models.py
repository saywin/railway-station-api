from django.test import TestCase

from station.models import TrainTypeModel


class TrainTypeModelTest(TestCase):
    def setUp(self):
        self.train_type = TrainTypeModel.objects.create(name="Light Rail")

    def test_create_train_type(self):
        train_type_2 = TrainTypeModel.objects.create(name="Heavy Rail")
        self.assertEqual(TrainTypeModel.objects.count(), 2)
        self.assertIn(self.train_type, TrainTypeModel.objects.all())
        self.assertIn(train_type_2, TrainTypeModel.objects.all())

    def test_train_type_str(self):
        self.assertEqual(str(self.train_type), self.train_type.name)

    def test_db_table_name(self):
        self.assertEqual(TrainTypeModel._meta.db_table, "train_type")
