from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint
from rest_framework.exceptions import ValidationError


class TrainTypeModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "train_type"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TrainModel(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        TrainTypeModel, on_delete=models.CASCADE, verbose_name="trains"
    )

    class Meta:
        db_table = "train"
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                fields=["cargo_num", "places_in_cargo"],
                name="unique_cargo_num_places_in_cargo",
            )
        ]

    def __str__(self):
        return self.name


class CrewModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "crew"
        ordering = ["last_name"]


class StationModel(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "station"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RouteModel(models.Model):
    source = models.ForeignKey(
        StationModel, on_delete=models.CASCADE, related_name="routers_from"
    )
    destination = models.ForeignKey(
        StationModel, on_delete=models.CASCADE, related_name="routers_to"
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"Source: {self.source.name}, destination: {self.destination.name}"

    class Meta:
        db_table = "route"


class JourneyModel(models.Model):
    route = models.ForeignKey(
        RouteModel, on_delete=models.CASCADE, related_name="journeys"
    )
    train = models.ForeignKey(
        TrainModel, on_delete=models.CASCADE, related_name="journeys"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crews = models.ManyToManyField(CrewModel, related_name="journeys")

    class Meta:
        db_table = "journey"

    def __str__(self):
        return (
            f"{self.route}, "
            f"departure: {self.departure_time}, "
            f"arrival: {self.arrival_time}"
        )


class OrderModel(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email}, {self.created_at}"


class TicketModel(models.Model):
    cargo = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    journey = models.ForeignKey(
        JourneyModel, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        OrderModel, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        db_table = "ticket"

    def __str__(self):
        return f"Order:{self.order.id}, cargo: {self.cargo}, seat: {self.seat}"

    def clean(self, *args, **kwargs):
        cargo_num = self.journey.train.cargo_num
        places_in_cargo = self.journey.train.places_in_cargo
        if not (1 <= self.cargo <= cargo_num):
            raise ValidationError(
                f"Cargo must be between [1, {cargo_num}]. Not {self.cargo}"
            )
        if not (1 <= self.seat <= places_in_cargo):
            raise ValidationError(
                f"Seat must be between [1, {places_in_cargo}]. Not {self.seat}"
            )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
