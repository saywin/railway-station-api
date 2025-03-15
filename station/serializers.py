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


