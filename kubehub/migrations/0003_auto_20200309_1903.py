# Generated by Django 3.0.3 on 2020-03-09 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kubehub', '0002_auto_20200226_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vm',
            name='cloud_provider_id',
        ),
        migrations.AddField(
            model_name='vm',
            name='cloud_provider',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.CloudProvider'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vmgroup',
            name='status',
            field=models.CharField(choices=[('creating', 'creating'), ('running', 'running'), ('removing', 'removing'), ('removed', 'removed'), ('error', 'error')], max_length=255),
        ),
    ]
