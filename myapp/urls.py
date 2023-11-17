from django.urls import path

from . import views
app_name = "inicio"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path('upload/', views.upload_file, name='upload_file'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('execute_code/', views.execute_code, name='execute_code'),
    path('test/', views.test, name='test'),    
    path('descargar_qrs/', views.descargar_imagenes_qr, name='descargar_qrs'),
    path('vehiculo/editar/<int:pk>/', views.editar_vehiculo, name='editar_vehiculo'),
]