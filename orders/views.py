from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, Ticket
from orders.serializers import (
    OrderListSerializer,
    OrderSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "tickets__flight__route__source",
            "tickets__flight__route__destination",
            "tickets__flight__airplane__airplane_type",
            "tickets__flight__crew",
        )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user).select_related(
            "flight__route__source",
            "flight__route__destination",
            "flight__airplane__airplane_type",
        )

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer