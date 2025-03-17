from django.urls import path, include
from rest_framework.routers import DefaultRouter

from station.views import (
    TrainTypeViewSet,
    TrainViewSet,
    CrewViewSet,
    StationViewSet,
    RouteViewSet,
    JourneyViewSet,
    OrderViewSet,
    TicketViewSet,
)

router = DefaultRouter()
router.register("train-type", TrainTypeViewSet, basename="train_type")
router.register("train", TrainViewSet, basename="train")
router.register("crew", CrewViewSet, basename="crew")
router.register("station", StationViewSet, basename="station")
router.register("route", RouteViewSet, basename="route")
router.register("journey", JourneyViewSet, basename="journey")
router.register("order", OrderViewSet, basename="order")
router.register("ticket", TicketViewSet, basename="ticket")

urlpatterns = [path("", include(router.urls))]

app_name = "station"
