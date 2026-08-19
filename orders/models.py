from aviation.models import Flight
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.email} ({self.created_at})"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def clean(self):
        # Check for row and seat not exeed airplane settings
        airplane = self.flight.airplane
        if not (1 <= self.row <= airplane.rows):
            raise ValidationError(
                {"row": f"Row must be between 1 and {airplane.rows}"}
            )
        if not (1 <= self.seat <= airplane.seats_in_row):
            raise ValidationError(
                {"seat": f"Seat must be between 1 and {airplane.seats_in_row}"}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flight} (Row: {self.row}, Seat: {self.seat})"
