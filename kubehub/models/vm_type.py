from django.db import models
from subprocess import check_output

from kubehub.models.os_image import OsImage
from kubehub.models.template import Template
from kubehub.vbox_api.models.vbox_img import VirtualBoxImage


class VmType(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    PLATFORM_CHOICES = (
        ('VirtualBox', 'VirtualBox'),
        ('Proxmox_image_based', 'Proxmox_image_based'),
        ('Proxmox_template_based', 'Proxmox_template_based')
    )
    platform_type = models.CharField(
        max_length=name_max,
        choices=PLATFORM_CHOICES
    )
    CORES_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4)
    )
    cores = models.IntegerField(
        choices=CORES_CHOICES
    )
    MEMORY_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4),
        (8, 8),
        (16, 16)
    )
    memory = models.IntegerField(
        choices=MEMORY_CHOICES
    )
    BOOT_DISK_CHOICES = (
        (32, 32),
        (64, 64),
        (128, 128),
        (256, 256),
        (512, 512)
    )
    boot_disk = models.IntegerField(
        choices=BOOT_DISK_CHOICES,
        default=32
    )
    proxmox_image = models.ForeignKey(
        to=OsImage,
        on_delete=models.PROTECT,
        null=True,
        default=None
    )
    proxmox_template = models.ForeignKey(
        to=Template,
        on_delete=models.PROTECT,
        null=True,
        default=None
    )
    vbox_image = models.ForeignKey(
        to=VirtualBoxImage,
        on_delete=models.PROTECT,
        null=True,
        default=None
    )

    readonly_fields = ('platform_type', 'cores', 'memory', 'boot_disk', 'proxmox_image',
                       'proxmox_template', 'vbox_image')

    def __str__(self):
        return f'id: {self.id}, platform_type: {self.platform_type}, cores: {self.cores}, memory: {self.memory},' \
               f'boot_disk: {self.boot_disk}, proxmox_image {self.proxmox_image}, ' \
               f'proxmox_template {self.proxmox_template}, vbox_image {self.vbox_image}'
