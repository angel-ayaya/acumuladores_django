# ======================================================
# Misceláneos
# ======================================================
from io import BytesIO
from django.core.files import File
from myapp.models import Vehiculo, QR
import os
from django.conf import settings
# ======================================================
# Librerias para generar el PDF
# ReportLab
# ======================================================
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# ======================================================
# Librerias para generar el código QR
# ======================================================
import qrcode
from PIL import Image, ImageDraw, ImageFont
# ======================================================

def get_data_from_db():
    pdfs_path = os.path.join(settings.MEDIA_ROOT, 'public')  # Ruta donde se guardarán los PDFs
    datos = Vehiculo.objects.all()
    encabezados = [
        "Placas",
        "Marca",
        "Sub Marca",
        "Serie Chasis",
        "Area",
        "Clave Acumulador"
    ]
    
    for vehiculo in datos:
        valores = [
            vehiculo.Placas,
            vehiculo.Marca,
            vehiculo.SubMarca,
            vehiculo.SerieChasis,
            vehiculo.Area,
            vehiculo.ClaveAcumulador
        ]
        id_acumulador = vehiculo.ClaveAcumulador

        # Crear una lista de datos para la tabla
        data = [encabezados]  # Agregar los encabezados como la primera fila
        data.append(valores)  # Agregar los valores como la segunda fila


        # Crear el pdf
        styles = getSampleStyleSheet()
        header_style = styles['Normal']
         # Aumentar el tamaño de fuente para los encabezados
        header_style.fontName = "Helvetica-Bold"  # Cambiar la fuente a negrita
        header_style.fontSize = 12  # Ajustar el tamaño de fuente según tus necesidades

        # Crea un color personalizado
        my_custom_color = colors.HexColor("#5e5a5c")
        bg_color = colors.HexColor("#f2f2f2")

         # Configura el estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (bg_color)),  # Fondo de la primera fila (encabezados)
            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),  # Color del texto de la primera fila
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la primera fila ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Fondo de las demás filas
            ('FONTSIZE', (0, 0), (-1, 0), header_style.fontSize),
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Líneas de la tabla
            ('SPLITBYROW', (0, 0), (-1, -1)),
            ('SPLITBYROWACTION', (0, 0), (-1, -1)),
            ('VALIGN', (0, 0), (0,0), 'MIDDLE')
        ])

        # Crear una tabla
        table = Table(data)
        table.setStyle(style)

        # Crear un documento PDF
        pdf_filename = f"{id_acumulador}.pdf"
        pdf_filepath = os.path.join(pdfs_path, f"{id_acumulador}.pdf")
        c = canvas.Canvas(pdf_filepath, pagesize=landscape(letter))

        # Calcular el ancho total de la página
        page_width, page_height = landscape(letter)

        # Obtener el ancho de la tabla
        table_width = table.wrap(0, 0)[0]
        # Obtener la altura de la tabla
        table_height = table.wrap(0, 0)[1]

        x = (page_width - table_width) / 2
        y = (page_height - table_height) / 2
        try:
            # Agregar la tabla al lienzo
            table.drawOn(c, x, y) 
            # Dibujar el logo
            c.drawImage("myapp/utils/logotipo.png", 25, 540, width=252.88, height=50, preserveAspectRatio=True)
            # Agregar la imagen del footer que ocupa el ancho total
            c.drawImage("myapp/utils/footer.jpg", 0, -25, width=page_width, height=169.93)
            c.setFont("Helvetica-Bold", 25)
            text_width = c.stringWidth("DATOS DEL ACUMULADOR", "Helvetica-Bold", 25)
            c.drawString((page_width - text_width)/2 , (page_height/2) + 125  , "DATOS DEL ACUMULADOR")
            # Dibujar una línea en la parte superior con un margen de 10 píxeles
            line_x_start = 25  # Margen izquierdo
            line_x_end = c._pagesize[0] - 25  # Margen derecho

            line_y = c._pagesize[1] - 50  # Margen superior 

            # Establecer el color personalizado como el color de la línea
            c.setStrokeColor(my_custom_color)
            c.setLineWidth(2)
            c.line((line_x_start * 2) + 252.88, line_y, line_x_end, line_y)


        except Exception as e:
            print("Error al cargar la imagen:", str(e))
            


        # Guardar el PDF y cerrar el lienzo
        c.showPage()
        c.save()

        # # Generar el código QR
        generar_qr(pdf_filename, id_acumulador)      

        print(f"Se ha creado el archivo PDF en formato horizontal: {pdf_filename}")


def qr_generator(pdf_filename, id_acumulador):    
    qrs_path = os.path.join(settings.MEDIA_ROOT, 'public/qrs')  # Ruta donde se guardarán los PDFs

    # Logo gobierno
    nombre_imagen = "logo.jpg"
    ruta_imagen = os.path.join(os.path.dirname(__file__), "utils/" + nombre_imagen)

    # Verificar si el archivo del logo existe
    if os.path.isfile(ruta_imagen):
        # Si el archivo existe, abrirlo
        logo = Image.open(ruta_imagen)
    else:
        # Si el archivo no existe, crea una imagen en blanco
        logo = Image.new('RGB', (100, 100), color='white')  # Cambia las dimensiones según tus necesidades


    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize))  # Aquí está la corrección
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    
    # taking url or text
    url = f'http://127.0.0.1:8000/media/public/{pdf_filename}'

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = 'Black'

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    # Agrega el texto que deseas mostrar debajo del código QR
    if id_acumulador is None:
        print("id_acumulador es nulo")
        # texto_debajo = ("undefined_" + str(idx))
    else:
        texto_debajo = id_acumulador

    # Crea un objeto ImageDraw para dibujar en la imagen
    draw = ImageDraw.Draw(QRimg)


    # Define la fuente y el tamaño del texto
    font = ImageFont.truetype("bahnschrift.ttf", 24)  # Puedes ajustar la fuente y el tamaño según tus preferencias

    # Calcula el largo de texto en pixeles
    
    text_lenght = draw.textlength(texto_debajo, font=font)
    # Calcula la posición donde deseas que aparezca el texto debajo del código QR
    x = (QRimg.width - text_lenght) // 2
    y = QRimg.height - 30 # Puedes ajustar la posición vertical según sea necesario
    # Dibuja el texto en la imagen
    draw.text((x, y), texto_debajo, fill="black", font=font)


    # Guardar el QR en un objeto BytesIO en lugar de un archivo directamente
    qr_io = BytesIO()
    QRimg.save(qr_io, format='PNG')
    qr_io.seek(0)  # Mover el cursor al inicio del archivo

    # Obtener o crear el objeto QR
    qr_obj, created = QR.objects.get_or_create(ClaveAcumulador=id_acumulador)

    # Guardar el objeto File en el campo QR del modelo
    qr_obj.QR.save(f"{id_acumulador}.png", File(qr_io))

    # No olvides cerrar el objeto BytesIO
    qr_io.close()


def generar_qr(pdf_filename, id_acumulador):
    try:
        qr_object = QR.objects.get(ClaveAcumulador=id_acumulador)
        if qr_object:
            print(qr_object.ClaveAcumulador)
        
        else:
            qr_generator(pdf_filename, id_acumulador)
            
    except QR.DoesNotExist:
        qr_generator(pdf_filename, id_acumulador)