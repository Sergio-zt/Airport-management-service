from aviation.serializers import FlightDetailSerializer, FlightSerializer
from rest_framework import serializers
from django.db import transaction
from orders.models import Order, Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Base serializer for ticket create"""

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, attrs):
        data = super().validate(attrs)
        # Check ticket
        ticket = Ticket(**attrs)
        try:
            ticket.clean()
        except Exception as e:
            raise serializers.ValidationError(
                e.message_dict if hasattr(e, 'message_dict') else str(e)
            )
        return data


class TicketListSerializer(TicketSerializer):
    """Base serializer for ticket list"""
    flight = FlightSerializer(read_only=True)


class TicketDetailSerializer(TicketSerializer):
    """Detail serialize for ticket"""
    flight = FlightDetailSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    # Add allow_empty=False, for prevent creation of empty order
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        # Витягуємо дані квитків із загального словника
        tickets_data = validated_data.pop("tickets")

        # Відкриваємо транзакцію
        with transaction.atomic():
            # Create order
            order = Order.objects.create(**validated_data)

            # List all tickets and add them to created order
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order


class OrderListSerializer(OrderSerializer):
    """Detail serializer for orders list with
    list of tickets and full info about flight"""
    tickets = TicketDetailSerializer(many=True, read_only=True)
