# Generated by Django 4.2.7 on 2023-11-09 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Placas', models.CharField(max_length=255)),
                ('Marca', models.CharField(max_length=255)),
                ('SubMarca', models.CharField(max_length=255)),
                ('SerieChasis', models.CharField(max_length=255)),
                ('Area', models.CharField(max_length=255)),
                ('ClaveAcumulador', models.CharField(max_length=255)),
            ],
        ),
    ]
