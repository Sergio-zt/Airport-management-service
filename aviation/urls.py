from django.urls import path, include

from rest_framework.routers import DefaultRouter

from aviation.views import (
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
    CountryViewSet,
    CityViewSet
)


app_name = "aviation"

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet, basename="airplanetype")
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
