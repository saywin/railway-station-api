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


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = JourneyModel.objects.all().select_related().prefetch_related("crews")
    serializer_class = JourneySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return self.serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = TicketModel.objects.all()
    serializer_class = TicketSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer

    #
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
