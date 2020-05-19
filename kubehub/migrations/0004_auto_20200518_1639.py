# Generated by Django 3.0.3 on 2020-05-18 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kubehub', '0003_virtualboxvm'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VMGroup',
            new_name='ProxmoxVmGroup',
        ),
        migrations.RemoveField(
            model_name='virtualboxvm',
            name='boot_disk',
        ),
        migrations.RemoveField(
            model_name='virtualboxvm',
            name='disk_type',
        ),
        migrations.RemoveField(
            model_name='virtualboxvm',
            name='sockets',
        ),
        migrations.RemoveField(
            model_name='virtualboxvm',
            name='vmid',
        ),
        migrations.AlterField(
            model_name='virtualboxvm',
            name='memory',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (4, 4), (8, 8), (16, 16)], default=1),
        ),
        migrations.CreateModel(
            name='VboxVmGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloud_provider', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.VirtualBoxCloudProvider')),
            ],
        ),
    ]