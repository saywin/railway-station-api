from django.contrib import admin

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

admin.site.register(TrainTypeModel)


@admin.register(TicketModel)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "cargo", "seat", "journey"]
    list_filter = ["journey"]
    list_editable = ["cargo", "seat"]


@admin.register(TrainModel)
class TrainAdmin(admin.ModelAdmin):
    list_display = ["name", "cargo_num", "places_in_cargo", "train_type"]
    list_filter = ["train_type"]
    search_fields = ["name", "train_type__name"]
    ordering = ["name"]


@admin.register(CrewModel)
class CrewAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]
    search_fields = ["first_name", "last_name"]
    ordering = ["first_name"]


@admin.register(StationModel)
class StationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "latitude", "longitude"]
    search_fields = ["name", "latitude", "longitude"]
    ordering = ["name"]


@admin.register(RouteModel)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "source", "destination", "distance"]


@admin.register(JourneyModel)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ["id", "route", "train", "departure_time", "arrival_time"]
    list_filter = ["route", "train"]


class TicketInline(admin.TabularInline):
    model = TicketModel
    fields = ["cargo", "seat", "journey", "order"]


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    list_display = ["id", "user", "created_at"]
