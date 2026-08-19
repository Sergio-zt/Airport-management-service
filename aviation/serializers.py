from rest_framework import serializers
from aviation.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Country,
    City
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityListSerializer(CitySerializer):
    country = serializers.CharField(source="country.name", read_only=True)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "closest_big_city")


class AirportListSerializer(AirportSerializer):
    city = serializers.CharField(source="city.name", read_only=True)
    country = serializers.CharField(source="city.country.name", read_only=True)

    class Meta(AirportSerializer.Meta):
        fields = ("id", "name", "city", "country")


class RouteSerializer(serializers.ModelSerializer):
    # Get full information about airport
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    # For writing transfer ID of airport
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), source='source', write_only=True
    )
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), source='destination', write_only=True
    )

    class Meta:
        model = Route
        fields = (
            'id',
            'source',
            'destination',
            'source_id',
            'destination_id',
            'distance'
        )


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.closest_big_city", read_only=True)
    destination = serializers.CharField(
        source="destination.closest_big_city", read_only=True
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('id', 'first_name', 'last_name')


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ('id', 'name')


class AirplaneSerializer(serializers.ModelSerializer):
    # Full information about type of airplane
    airplane_type = AirplaneTypeSerializer(read_only=True)
    airplane_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all(),
        source="airplane_type",
        write_only=True,
    )
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "airplane_type_id",
            "capacity",
        )


class FlightSerializer(serializers.ModelSerializer):

    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), source="route", write_only=True
    )
    airplane_id = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all(), source="airplane", write_only=True
    )
    crew_ids = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), source="crew", many=True, write_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route_id",
            "airplane_id",
            "departure_time",
            "arrival_time",
            "crew_ids",
        )


class FlightListSerializer(FlightSerializer):

    route = RouteListSerializer(read_only=True)
    airplane_name = serializers.CharField(
        source="airplane.name", read_only=True
    )
    airplane_capacity = serializers.IntegerField(
        source="airplane.capacity", read_only=True
    )
    crew_count = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane_name",
            "airplane_capacity",
            "departure_time",
            "arrival_time",
            "crew_count",
        )

    def get_crew_count(self, obj):
        return obj.crew.count()


class FlightDetailSerializer(FlightSerializer):

    route = RouteSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )
