from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Airplane, AirplaneType, Airport, Crew, Flight, Route
from .serializers import (
    AirplaneSerializer,
    AirplaneTypeSerializer,
    AirportSerializer,
    CrewSerializer,
    FlightSerializer,
    RouteSerializer,
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination").all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type").all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects.select_related(
            "route__source", "route__destination", "airplane__airplane_type"
        )
        .prefetch_related("crew")
        .all()
    )
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
