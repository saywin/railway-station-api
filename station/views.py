from django.shortcuts import render
from rest_framework import viewsets

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
from station.serializers import (
    TrainTypeSerializer,
    TrainListSerializer,
    TrainSerializer,
    TrainDetailSerializer,
    CrewSerializer,
    StationSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    JourneySerializer,
    JourneyListSerializer,
    JourneyDetailSerializer,
    OrderSerializer,
    TicketSerializer,
)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainTypeModel.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = TrainModel.objects.select_related()
    serializer_class = TrainListSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.action == "list":
            return TrainListSerializer
        if self.action == "retrieve":
            return TrainDetailSerializer
        return self.serializer_class


class CrewViewSet(viewsets.ModelViewSet):
    queryset = CrewModel.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = StationModel.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = RouteModel.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("source", "destination")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


# Create your views here.
