from django.urls import path
from views import (
    AirportView,
)


app_name = "airports"

urlpatterns = [
    path("airport/", AirportView.as_view(), name="airport"),
]