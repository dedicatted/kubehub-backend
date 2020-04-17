from django.db import models
from subprocess import check_output

from ..models.proxmox_cloud_provider import ProxmoxCloudProvider
from ..models.vm_group import VMGroup


class VM(models.Model):
    class Meta:
        abstract = True
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE, related_name="vms")
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    ip = models.CharField(max_length=name_max)
    cloud_provider = models.ForeignKey(ProxmoxCloudProvider, on_delete=models.PROTECT, related_name="vms")
    CORES_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4)
    )
    cores = models.IntegerField(
        choices=CORES_CHOICES,
        default=1
    )
    SOCKETS_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4)
    )
    sockets = models.IntegerField(
        choices=SOCKETS_CHOICES,
        default=1
    )
    MEMORY_CHOICES = (
        (1024, 1024),
        (2048, 2048),
        (4096, 4096),
        (8192, 8192),
        (16384, 16384)
    )
    memory = models.IntegerField(
        choices=MEMORY_CHOICES,
        default=1024
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
    DISK_TYPE_CHOICES = (
        ('scsi0', 'scsi0'),
        ('virtio0', 'virtio0'),
        ('ide0', 'ide0'),
        ('sata0', 'sata0')
    )
    disk_type = models.CharField(
        max_length=name_max,
        choices=DISK_TYPE_CHOICES,
        default='scsi0'
    )

    readonly_fields = ('vm_group_id', 'name', 'vmid', 'ip', 'cloud_provider',
                       'cores', 'sockets', 'memory', 'boot_disk', 'disk_type')

    def __str__(self):
        return f'id: {self.id}, vm_group_id: {self.vm_group.id} name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, ' \
               f'cloud_provider: {self.cloud_provider}, cores: {self.cores}, sockets: {self.sockets}, ' \
               f'memory: {self.memory}, boot_disk: {self.boot_disk},'




