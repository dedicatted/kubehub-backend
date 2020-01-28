# Generated by Django 3.0.2 on 2020-01-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kubehub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloudprovider',
            name='cp_type',
            field=models.CharField(choices=[('PROX_MOX', 'PROX_MOX'), ('AWS', 'AWS'), ('GCP', 'GCP')], max_length=20),
        ),
    ]