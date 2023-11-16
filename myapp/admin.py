from django.contrib import admin

# Register your models here.
from .models import Question, Vehiculo, QR

admin.site.register(Question)
admin.site.register(Vehiculo)
admin.site.register(QR)