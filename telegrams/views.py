from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .utils.pdf_generator import generar_telegrama_pdf
import os
import tempfile


@login_required
def dashboard(request):
    return render(request, "telegrams/dashboard.html")


@login_required
def create_telegram(request):
    return render(request, "telegrams/create_telegram.html")


@login_required
def generate_pdf(request):

    if request.method != "POST":
        return HttpResponse("Método no permitido", status=405)

    # Datos del formulario
    datos = {
        "dest_nombre": request.POST.get("dest_nombre", ""),
        "dest_ramo": request.POST.get("dest_ramo", ""),
        "dest_domicilio_laboral": request.POST.get("dest_domicilio_laboral", ""),
        "dest_cp": request.POST.get("dest_cp", ""),
        "dest_localidad": request.POST.get("dest_localidad", ""),
        "dest_provincia": request.POST.get("dest_provincia", ""),

        "rem_nombre": request.POST.get("rem_nombre", ""),
        "rem_dni": request.POST.get("rem_dni", ""),
        "rem_fecha": request.POST.get("rem_fecha", ""),
        "rem_domicilio_real": request.POST.get("rem_domicilio_real", ""),
        "rem_cp": request.POST.get("rem_cp", ""),
        "rem_localidad": request.POST.get("rem_localidad", ""),
        "rem_provincia": request.POST.get("rem_provincia", ""),

        "cuerpo": request.POST.get("cuerpo", ""),
        "tipo_comunicacion": request.POST.get("tipo_comunicacion", "1"),
    }

    # Ruta absoluta de plantilla.jpg
    plantilla_path = os.path.join(
        settings.BASE_DIR,
        "staticfiles",
        "telegram_bg",
        "plantilla.jpg"
    )

    # Generar archivo temporal
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    generar_telegrama_pdf(temp.name, plantilla_path, datos)

    # Enviar PDF al usuario
    with open(temp.name, "rb") as f:
        pdf_data = f.read()

    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="telegrama.pdf"'

    return response
