from django.urls import path, include

from rest_framework.routers import DefaultRouter

from airports.views import (
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
)


app_name = "airports"

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet, basename="airplanetype")
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]