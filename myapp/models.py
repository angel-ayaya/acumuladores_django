"""Modelos de la aplicación"""
from django.db import models

class Question(models.Model):
    """Modelo de pregunta"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.question_text)

class Vehiculo(models.Model):
    """Modelo de vehiculo"""
    Placas = models.CharField(max_length=255)
    Marca = models.CharField(max_length=255)
    SubMarca = models.CharField(max_length=255)
    SerieChasis = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    ClaveAcumulador = models.CharField(max_length=255)

    def __str__(self):
        return str(self.ClaveAcumulador)

class QR(models.Model):
    """Modelo de QR"""
    ClaveAcumulador = models.CharField(max_length=255)
    QR = models.ImageField(upload_to='public/qrs')

    def __str__(self):
        return str(self.ClaveAcumulador)
