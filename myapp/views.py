
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.core.files.storage import FileSystemStorage
from myapp.models import Vehiculo
from .forms import VehiculoForm

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from django.conf import settings
from django.templatetags.static import static

from . import qr_generation as qr

import pandas as pd
from .models import Vehiculo, QR
from .forms import QrForm

# ======================================================
# Descargar imágenes QR masivamente
import zipfile
from io import BytesIO
# ======================================================

def inicio(request):

    search_term = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'claveacumulador')

    vehiculos = Vehiculo.objects.all()

    if search_term:
        if filter_type == 'placas':
            vehiculos = vehiculos.filter(Placas__icontains=search_term)
        elif filter_type == 'marca':
            vehiculos = vehiculos.filter(Marca__icontains=search_term)
        elif filter_type == 'submarca':
            vehiculos = vehiculos.filter(SubMarca__icontains=search_term)
        elif filter_type == 'seriechasis':
            vehiculos = vehiculos.filter(SerieChasis__icontains=search_term)
        elif filter_type == 'area':
            vehiculos = vehiculos.filter(Area__icontains=search_term)
        elif filter_type == 'claveacumulador':
            vehiculos = vehiculos.filter(ClaveAcumulador__icontains=search_term)
        elif filter_type == '':
            pass

    ctx = {
        'vehiculos': vehiculos
        }
    
    return render(request, "inicio.html", ctx)

def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('inicio:inicio')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'editar_vehiculo.html', {'form': form})

def upload_file(request):
     # Obtener todas las claves acumuladoras existentes en la base de datos
    claves_acumuladoras_exist = list(Vehiculo.objects.values_list('ClaveAcumulador', flat=True))

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        df = pd.read_excel(uploaded_file)

        for index, row in df.iterrows():
            clave_acumulador = row["CLAVE ACUMULADOR"]
            placa = row["Placas"]
            if not pd.isnull(clave_acumulador):
                if clave_acumulador in claves_acumuladoras_exist:
                    print(f"La clave acumuladora {clave_acumulador} ya existe en la base de datos.")
                    print(f"El coche con placa {placa} no se ha guardado debido a una duplicación de clave acumuladora.")
                else:
                    claves_acumuladoras_exist.append(clave_acumulador)
                    coche = Vehiculo(
                        Placas=row["Placas"],
                        Marca=row["Marca"],
                        SubMarca=row["Sub-Marca"],
                        SerieChasis=row["Serie Chasis"],
                        Area=row["Area"],
                        ClaveAcumulador=row["CLAVE ACUMULADOR"]
                    )
                    coche.save()
    
    return render(request, 'upload.html')

def catalogue(request):
    codigos_qr = QR.objects.all()

    
    context = {'codigos_qr': codigos_qr}

    return render(request, 'catalogue.html', context)

def execute_code(request):
    qr.get_data_from_db()
    return redirect('/catalogue')

def descargar_imagenes_qr(request):
    # Directorio donde se encuentran las imágenes
    dir_imagenes = os.path.join(settings.MEDIA_ROOT, 'public', 'qrs')

    # Crear un buffer de bytes para el archivo ZIP
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for filename in os.listdir(dir_imagenes):
            if filename.endswith('.png'):  # Asegúrate de ajustar la extensión de archivo si es necesario
                filepath = os.path.join(dir_imagenes, filename)
                zip_file.write(filepath, filename)

    # Establecer el puntero del buffer al principio del stream
    buffer.seek(0)

    # Crear la respuesta HTTP con el archivo ZIP
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="imagenes_qr.zip"'

    return response

def generate_pdf():
    pass

def navbar(request):
    return render(request, 'navbar.html')

def search(request):
    #return an url in another tab
    # url = 
    return redirect('/catalogue')

def test(request):
    search_term = request.GET.get('search', '')  # Obtiene el término de búsqueda del query string
    vehiculos = Vehiculo.objects.all()
    codigos_qr = QR.objects.all()
      
    if search_term:
        vehiculos = vehiculos.filter(ClaveAcumulador__icontains=search_term)
    
    ctx = {
        'vehiculos': vehiculos,
        'codigos_qr': codigos_qr
        }
    
    return render(request, 'test.html', ctx)