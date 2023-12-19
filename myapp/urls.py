"""myapp URL Configuration"""
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views  # Asegúrate de importar tus vistas

app_name = "inicio"

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('', views.inicio_redirect, name='inicio_redirect'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio:login'), name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('execute_code/', views.execute_code, name='execute_code'),
    path('test/', views.test, name='test'),    
    path('descargar_qrs/', views.descargar_imagenes_qr, name='descargar_qrs'),
    path('vehiculo/editar/<int:pk>/', views.editar_vehiculo, name='editar_vehiculo'),

path('descargar-template/', serve, {'document_root': settings.MEDIA_ROOT, 'path': 'public/acumuladores.xlsx'}, name='descargar_template'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
