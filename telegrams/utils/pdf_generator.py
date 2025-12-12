from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
import io
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# Tamaño A4 en puntos
A4_WIDTH, A4_HEIGHT = A4  # 595 x 842 pt


def generar_telegrama_pdf(output_path, plantilla_path, datos):
    """
    Genera el PDF del telegrama usando la plantilla como fondo.
    """
    # Crear canvas
    c = canvas.Canvas(output_path, pagesize=A4)

    # --- 1) Fondo completo ---
    fondo = ImageReader(plantilla_path)
    c.drawImage(
        fondo,
        0,            # x
        0,            # y
        width=A4_WIDTH,
        height=A4_HEIGHT
    )

    # Configuración general
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 10)

    # ===============================
    #   COORDENADAS EXACTAS
    # ===============================

    # DESTINATARIO
    c.drawString(30, 842 - 115, datos["dest_nombre"])
    c.drawString(30, 842 - 144, datos["dest_ramo"])
    c.drawString(30, 842 - 173, datos["dest_domicilio_laboral"])
    c.drawString(213, 842 - 173, datos["dest_cp"])
    c.drawString(30, 842 - 201, datos["dest_localidad"])
    c.drawString(213, 842 - 201, datos["dest_provincia"])

    # REMITENTE
    c.drawString(312, 842 - 115, datos["rem_nombre"])
    c.drawString(312, 842 - 144, datos["rem_dni"])
    c.drawString(498, 842 - 144, datos["rem_fecha"])
    c.drawString(312, 842 - 173, datos["rem_domicilio_real"])
    c.drawString(498, 842 - 173, datos["rem_cp"])
    c.drawString(312, 842 - 201, datos["rem_localidad"])
    c.drawString(498, 842 - 201, datos["rem_provincia"])

    # ===============================
    #  CUERPO DEL TELEGRAMA
    # ===============================

    texto_original = datos["cuerpo"]
    texto_html = texto_original.replace("\n", "<br/>")

    # Dibujar el cuerpo con auto-ajuste
    dibujar_cuerpo(c, texto_html)

    # ==========================================================
    #  TIPO DE COMUNICACIÓN (marcar el círculo correspondiente)
    # ==========================================================

    # Coordenadas de los tres círculos
    circulos = {
        "renuncia": (173, 842 - 734),
        "ausencia": (368, 842 - 734),
        "otro": (559, 842 - 734)
    }

    # Radios del círculo
    radio = 5

    # Dibujar los tres círculos vacíos
    for (cx, cy) in circulos.values():
        c.circle(cx, cy, radio, stroke=1, fill=0)

    # Rellenar solo el seleccionado
    seleccion = str(datos.get("tipo_comunicacion", ""))

    if seleccion in circulos:
        cx, cy = circulos[seleccion]
        c.circle(cx, cy, radio, stroke=0, fill=1)  # círculo negro

    # Cerrar PDF
    c.showPage()
    c.save()



# ================================================================
# ===============   FUNCIÓN QUE AUTO-AJUSTA EL TEXTO   ===========
# ================================================================
def dibujar_cuerpo(c, texto_html):

    # ======== ÁREA DEL RECUADRO ========
    x = 32
    y = 842 - 670
    ancho = 540
    alto = 420

    # ======== TAMAÑOS A PROBAR ========
    # (primero grande → luego más chico)
    sizes = [12, 11, 10, 9, 8, 7, 6, 5]

    def crear_paragraph(size):
        """Crea un Paragraph con el tamaño indicado."""
        style = ParagraphStyle(
            name="CuerpoTelegrama",
            fontName="Helvetica",
            fontSize=size,
            leading=size + 2,     # interlineado apenas mayor para legibilidad
            alignment=TA_LEFT,
        )
        return Paragraph(texto_html, style)

    def entra(paragraph):
        """
        Usa paragraph.split() para ver si entra EN EL MISMO FRAME,
        sin dibujar, sin canvas temporal, sin mover el frame.
        """
        parts = paragraph.split(ancho, alto)

        # Si split devuelve 1 elemento, entra entero
        return len(parts) == 1

    # ======== PROBAR TAMAÑO DE FUENTE DE MAYOR A MENOR ========
    for size in sizes:
        par = crear_paragraph(size)

        if entra(par):
            # ----- ENTRA PERFECTO → SE DIBUJA -----
            frame_real = Frame(x, y, ancho, alto, showBoundary=0)
            frame_real.addFromList([par], c)
            return

    # ======== SI NO ENTRA NI EN SIZE 5, DIBUJAR IGUAL ========
    par = crear_paragraph(5)
    frame_real = Frame(x, y, ancho, alto, showBoundary=0)
    frame_real.addFromList([par], c)


