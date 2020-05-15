# Generated by Django 3.0.3 on 2020-05-14 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kubehub', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='virtualboxcloudprovider',
            old_name='vbox_img_dir',
            new_name='image_folder',
        ),
        migrations.AddField(
            model_name='virtualboxcloudprovider',
            name='machine_folder',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
