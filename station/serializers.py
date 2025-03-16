from rest_framework import serializers

from station.models import (
    TrainTypeModel,
    TrainModel,
    CrewModel,
    StationModel,
    RouteModel,
    JourneyModel,
    OrderModel,
    TicketModel,
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainTypeModel
        fields = ["id", "name"]


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainModel
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(read_only=True, slug_field="name")


class TrainDetailSerializer(TrainSerializer):
    train_type = TrainTypeSerializer()


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewModel
        fields = ["id", "first_name", "last_name", "full_name"]


class CrewFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewModel
        fields = ["full_name"]


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationModel
        fields = ["id", "name", "latitude", "longitude"]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteModel
        fields = ["id", "source", "destination", "distance"]


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(slug_field="name", read_only=True)
    destination = serializers.SlugRelatedField(slug_field="name", read_only=True)


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyModel
        fields = ["id", "route", "train", "departure_time", "arrival_time", "crews"]


class JourneyListSerializer(serializers.ModelSerializer):
    route_from = serializers.SlugRelatedField(
        slug_field="source.name", source="route", read_only=True
    )
    route_to = serializers.SlugRelatedField(
        slug_field="destination.name", source="route", read_only=True
    )
    train_name = serializers.SlugRelatedField(
        slug_field="name", source="train", read_only=True
    )
    crews = serializers.SlugRelatedField(
        slug_field="full_name", many=True, read_only=True
    )

    class Meta:
        model = JourneyModel
        fields = [
            "id",
            "train_name",
            "route_from",
            "route_to",
            "departure_time",
            "arrival_time",
            "crews",
        ]


class JourneyDetailSerializer(JourneySerializer):
    train = TrainDetailSerializer()
    route = RouteDetailSerializer()
    crews = CrewSerializer(many=True, read_only=True)


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        max_cargo = attrs["journey"].train.cargo_num
        max_seat = attrs["journey"].train.places_in_cargo
        TicketModel.validate_max_value_num(
            num=attrs["cargo"],
            max_num=max_cargo,
            error=serializers.ValidationError,
            name="Cargo",
        )
        TicketModel.validate_max_value_num(
            num=attrs["seat"],
            max_num=max_seat,
            error=serializers.ValidationError,
            name="Seat",
        )
        return super().validate(attrs)

    class Meta:
        model = TicketModel
        fields = ["id", "cargo", "seat", "journey", "order"]


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer()


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=False, allow_empty=False)

    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        order = OrderModel.objects.create(**validated_data)
        for ticket in tickets:
            ticket.pop("order", None)
            TicketModel.objects.create(order=order, **ticket)
        return order

    class Meta:
        model = OrderModel
        fields = ["id", "created_at", "tickets"]
