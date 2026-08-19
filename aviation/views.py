from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrIfAuthenticatedReadOnly
from aviation.models import (
   Airplane,
   AirplaneType,
   Airport,
   Crew,
   Flight,
   Route,
   Country,
   City
)
from aviation.serializers import (
    AirplaneSerializer,
    AirplaneTypeSerializer,
    AirportSerializer,
    AirportListSerializer,
    CrewSerializer,
    FlightSerializer,
    RouteSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    CitySerializer,
    CountrySerializer,
    CityListSerializer
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country").all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CityListSerializer
        return CitySerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city__country").all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AirportListSerializer
        return AirportSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination").all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type").all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class FlightViewSet(viewsets.ModelViewSet):
  queryset = (
      Flight.objects.select_related(
          "route__source", "route__destination", "airplane__airplane_type"
      )
      .prefetch_related("crew")
      .all()
  )
  permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

  def get_serializer_class(self):
    if self.action == "list":
      return FlightListSerializer

    if self.action == "retrieve":
      return FlightDetailSerializer

    return FlightSerializer
