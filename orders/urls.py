from django.urls import include, path
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet, TicketViewSet

app_name = "orders"

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]
