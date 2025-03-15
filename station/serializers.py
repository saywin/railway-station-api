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
