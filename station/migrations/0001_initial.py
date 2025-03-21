# Generated by Django 5.1.7 on 2025-03-14 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrewModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "crew",
                "ordering": ["last_name"],
            },
        ),
        migrations.CreateModel(
            name="OrderModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "order",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="RouteModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("distance", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "route",
            },
        ),
        migrations.CreateModel(
            name="StationModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
            options={
                "db_table": "station",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="TicketModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cargo", models.PositiveIntegerField()),
                ("seat", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ticket",
            },
        ),
        migrations.CreateModel(
            name="TrainModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("cargo_num", models.PositiveIntegerField()),
                ("places_in_cargo", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "train",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="TrainTypeModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "train_type",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="JourneyModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure_time", models.DateTimeField()),
                ("arrival_time", models.DateTimeField()),
                (
                    "crews",
                    models.ManyToManyField(
                        related_name="journeys", to="station.crewmodel"
                    ),
                ),
            ],
            options={
                "db_table": "journey",
            },
        ),
    ]
