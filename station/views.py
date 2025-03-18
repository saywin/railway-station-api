from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
    # TicketListSerializer,
    TrainImageSerializer,
    StationImageSerializer,
    TicketListSerializer,
    OrderListSerializer,
)


def image_upload(obj, serializer, data):
    train = obj
    serializer = serializer(train, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


@extend_schema(tags=["Train Type API"])
class TrainTypeViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = TrainTypeModel.objects.all()
    serializer_class = TrainTypeSerializer


@extend_schema(tags=["Train API"])
class TrainViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = TrainModel.objects.all()
    serializer_class = TrainSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ["retrieve", "list"]:
            queryset = queryset.select_related()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        if self.action == "retrieve":
            return TrainDetailSerializer
        if self.action == "upload_image":
            return TrainImageSerializer
        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="train-image",
    )
    def upload_image(self, request, pk=None):
        train = self.get_object()
        serializer = self.get_serializer(train, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Crew API"])
class CrewViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = CrewModel.objects.all()
    serializer_class = CrewSerializer


@extend_schema(tags=["Station API"])
class StationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = StationModel.objects.all()
    serializer_class = StationSerializer

    def get_serializer_class(self):
        if self.action == "upload_image":
            return StationImageSerializer
        return StationSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="station-image",
    )
    def upload_image(self, request, pk=None):
        station = self.get_object()
        serializer = self.get_serializer(station, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Route API"])
class RouteViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = RouteModel.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = self.queryset

        source = self.request.query_params.get("source")
        if source:
            queryset = queryset.filter(source__name__icontains=source)

        destination = self.request.query_params.get("destination")
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("source", "destination")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                description="Filter by source",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="destination",
                description="Filter by destination",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """List Route with filter by source and destination"""
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Journey API"])
class JourneyViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = JourneyModel.objects.all()
    serializer_class = JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=F("train__cargo_num") * F("train__places_in_cargo")
                - Count("tickets")
            )

        departure_time = self.request.query_params.get("date")
        if departure_time:
            queryset = queryset.filter(departure_time__date=departure_time)

        route_from = self.request.query_params.get("from")
        if route_from:
            queryset = queryset.filter(route__source__name__icontains=route_from)

        route_to = self.request.query_params.get("to")
        if route_to:
            queryset = queryset.filter(route__destination__name__icontains=route_to)

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related().prefetch_related("crews")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="from",
                description="Filter by route_from (ex. ?from='Dnipro')",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="to",
                description="Filter by route_to (ex. ?to='Kyiv')",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="date",
                description="Filter by date (ex. ?date='2023-06-12')",
                required=False,
                type=OpenApiTypes.DATE,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """List Journey with filter by route_from, route_to and date"""
        return super().list(request, *args, **kwargs)


class OrderSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 1000


@extend_schema(tags=["Order API"])
class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action in ["list", "retrieve"]:
            queryset = queryset.prefetch_related("tickets__journey__crews")
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
