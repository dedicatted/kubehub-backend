# Generated by Django 3.0.3 on 2020-03-27 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kubehub', '0014_kubernetesversion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kubernetescluster',
            name='k8s_version',
        ),
        migrations.AddField(
            model_name='kubernetescluster',
            name='kubernetes_version',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='kubehub.KubernetesVersion'),
            preserve_default=False,
        ),
    ]