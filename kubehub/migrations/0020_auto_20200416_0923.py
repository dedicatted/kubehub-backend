# Generated by Django 3.0.3 on 2020-04-16 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kubehub', '0019_vmfromtemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxmoxCloudProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cp_type', models.CharField(choices=[('Proxmox', 'Proxmox'), ('AWS', 'AWS'), ('GCP', 'GCP')], max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('api_endpoint', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('shared_storage_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='vmfromimage',
            name='cloud_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.ProxmoxCloudProvider'),
        ),
        migrations.AlterField(
            model_name='vmfromtemplate',
            name='cloud_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.ProxmoxCloudProvider'),
        ),
        migrations.DeleteModel(
            name='CloudProvider',
        ),
    ]