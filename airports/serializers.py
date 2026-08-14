from rest_framework import serializers
from .models import Airport, Route, Crew, AirplaneType, Airplane, Flight


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('id', 'name', 'closest_big_city')


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
        queryset=AirplaneType.objects.all(), source='airplane_type', write_only=True
    )
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            'id', 
            'name', 
            'rows', 
            'seats_in_row', 
            'airplane_type', 
            'airplane_type_id', 
            'capacity'
        )


class FlightSerializer(serializers.ModelSerializer):
    # Included data about route
    route = RouteSerializer(read_only=True)
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), source='route', write_only=True
    )
    
    airplane = AirplaneSerializer(read_only=True)
    airplane_id = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all(), source='airplane', write_only=True
    )
    
    crew = CrewSerializer(many=True, read_only=True)
    crew_ids = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), source='crew', many=True, write_only=True
    )

    class Meta:
        model = Flight
        fields = (
            'id', 
            'route', 
            'route_id', 
            'airplane', 
            'airplane_id', 
            'departure_time', 
            'arrival_time', 
            'crew', 
            'crew_ids'
        )
