from django.shortcuts import render

from .models import Portal


def inicio(request):
    portales = Portal.objects.filter(activo=True)

    return render(
        request,
        "portales/index.html",
        {
            "portales": portales,
        },
    )