from django.db import models
from django.conf import settings

class Telegram(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="telegrams"
    )

    # ------------------------
    # DESTINATARIO
    # ------------------------
    dest_nombre = models.CharField(max_length=200)
    dest_ramo = models.CharField(max_length=200, blank=True)
    dest_domicilio_laboral = models.CharField(max_length=300)
    dest_cp = models.CharField(max_length=20)
    dest_localidad = models.CharField(max_length=200)
    dest_provincia = models.CharField(max_length=200)

    # ------------------------
    # REMITENTE
    # ------------------------
    rem_nombre = models.CharField(max_length=200)
    rem_dni = models.CharField(max_length=20)
    rem_fecha = models.CharField(max_length=20)
    rem_domicilio_real = models.CharField(max_length=300)
    rem_cp = models.CharField(max_length=20)
    rem_localidad = models.CharField(max_length=200)
    rem_provincia = models.CharField(max_length=200)

    # ------------------------
    # CUERPO DEL TELEGRAMA
    # ------------------------
    cuerpo = models.TextField()

    # ------------------------
    # TIPO DE COMUNICACIÓN
    # ------------------------
    tipo_comunicacion = models.CharField(
        max_length=20,
        choices=[
            ("renuncia", "Comunicación de renuncia"),
            ("ausencia", "Comunicación de ausencia"),
            ("otro", "Otro tipo de comunicación"),
        ]
    )

    # ------------------------
    # TAMAÑOS DE FUENTE PERSONALIZABLES
    # ------------------------
    font_destinatario = models.IntegerField(default=12)
    font_remitente = models.IntegerField(default=12)
    font_cuerpo = models.IntegerField(default=12)
    font_tipo = models.IntegerField(default=12)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Telegrama {self.id} - {self.user.username}"
