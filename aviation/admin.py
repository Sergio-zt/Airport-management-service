from django.contrib import admin
from aviation.models import (
    Country, City, Airport, Route,
    AirplaneType, Airplane, Crew, Flight
)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city", "city")
    search_fields = ("name",)


# Регистрируем остальные модели
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(Flight)
