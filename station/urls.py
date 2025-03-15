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
router.register("train-type", TrainTypeViewSet)
router.register("train", TrainViewSet)
router.register("crew", CrewViewSet)
router.register("station", StationViewSet)
router.register("route", RouteViewSet)
router.register("journey", JourneyViewSet)
router.register("order", OrderViewSet)
router.register("ticket", TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "station"
