from django.contrib import admin

from .models import Portal


@admin.register(Portal)
class PortalAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "categoria",
        "url",
        "activo",
        "fecha_actualizacion",
    )

    list_filter = (
        "categoria",
        "activo",
    )

    search_fields = (
        "nombre",
        "url",
        "descripcion",
    )

    readonly_fields = (
        "categoria",
        "icono",
        "fecha_creacion",
        "fecha_actualizacion",
    )

    ordering = (
        "nombre",
    )