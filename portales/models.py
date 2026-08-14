from urllib.parse import urlparse

from django.db import models


class Portal(models.Model):

    CATEGORIAS = [
        ("intra", "INTRA"),
        ("orbita", "Órbita"),
        ("nom035", "NOM035"),
        ("contabilidad", "Contabilidad"),
        ("collaboracali", "Collaboracali"),
    ]

    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre del portal"
    )

    url = models.URLField(
        max_length=500,
        verbose_name="URL"
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )

    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIAS,
        verbose_name="Categoría"
    )

    icono = models.CharField(
        max_length=100,
        default="fa-solid fa-globe",
        verbose_name="Icono FontAwesome"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Portal activo"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = "Portal"

        verbose_name_plural = "Portales"

        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


    # =====================================================
    # DETECTAR CATEGORÍA AUTOMÁTICAMENTE
    # =====================================================

    def detectar_categoria(self):

        url = self.url.lower().strip()

        # Quitamos protocolo para facilitar la comparación
        dominio = urlparse(url).netloc.lower()

        # -------------------------------------------------
        # COLLABORACALI
        # -------------------------------------------------

        if "collaboracali.com" in dominio:
            return "collaboracali"


        # -------------------------------------------------
        # ÓRBITA
        # -------------------------------------------------

        if "orbita.now" in dominio:
            return "orbita"


        # -------------------------------------------------
        # NOM035
        # -------------------------------------------------

        if (
            "nom035" in dominio
            or "nom-035" in dominio
            or "nom.intra.org.mx" in dominio
        ):
            return "nom035"


        # -------------------------------------------------
        # CONTABILIDAD
        # -------------------------------------------------

        nombre = self.nombre.lower()

        if (
            "contable" in nombre
            or "contabilidad" in nombre
            or "legacy" in nombre
        ):
            return "contabilidad"


        # -------------------------------------------------
        # INTRA
        # -------------------------------------------------

        if (
            "intra.org.mx" in dominio
            or "grupointra.mx" in dominio
        ):
            return "intra"


        # -------------------------------------------------
        # SI NO SE PUEDE IDENTIFICAR
        # -------------------------------------------------

        return self.categoria


    # =====================================================
    # DETECTAR ICONO AUTOMÁTICAMENTE
    # =====================================================

    def detectar_icono(self, categoria):

        iconos = {

            "intra":
                "fa-solid fa-building",

            "orbita":
                "fa-solid fa-globe",

            "nom035":
                "fa-solid fa-shield-heart",

            "contabilidad":
                "fa-solid fa-calculator",

            "collaboracali":
                "fa-solid fa-users",

        }

        return iconos.get(
            categoria,
            "fa-solid fa-globe"
        )


    # =====================================================
    # GUARDADO AUTOMÁTICO
    # =====================================================

    def save(self, *args, **kwargs):

        # Detectar categoría según URL/nombre
        categoria_detectada = self.detectar_categoria()

        self.categoria = categoria_detectada

        # Asignar icono automáticamente
        self.icono = self.detectar_icono(
            categoria_detectada
        )

        super().save(*args, **kwargs)