from django.contrib import admin
from orders.models import Order, Ticket


class TicketInline(admin.TabularInline):
    """Allow to add tickets in order"""
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    inlines = (TicketInline,)


admin.site.register(Ticket)
