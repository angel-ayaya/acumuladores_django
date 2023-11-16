import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text

    
class Vehiculo(models.Model):
    Placas = models.CharField(max_length=255)
    Marca = models.CharField(max_length=255)
    SubMarca = models.CharField(max_length=255)
    SerieChasis = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    ClaveAcumulador = models.CharField(max_length=255)

    def __str__(self):
        return self.ClaveAcumulador

class QR(models.Model):
    ClaveAcumulador = models.CharField(max_length=255)
    QR = models.ImageField(upload_to='public/qrs')

    def __str__(self):
        return self.ClaveAcumulador