from django.contrib import admin

from game.models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("city", "country")
    search_fields = ("city", "country")
