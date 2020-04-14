from django.db import models
from subprocess import check_output

from ..models.cloud_provider import CloudProvider
from ..models.vm_group import VMGroup


class VM(models.Model):
    name_max = int(check_output("getconf NAME_MAX /", shell=True))
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE, related_name="vms")
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    ip = models.CharField(max_length=name_max)
    cloud_provider = models.ForeignKey(CloudProvider, on_delete=models.PROTECT, related_name="vms")
    CORES_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4)
    )
    cores = models.IntegerField(choices=CORES_CHOICES)
    SOCKETS_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4)
    )
    sockets = models.IntegerField(choices=SOCKETS_CHOICES)
    MEMORY_CHOICES = (
        (1024, 1024),
        (2048, 2048),
        (4096, 4096),
        (8192, 8192)
    )
    memory = models.IntegerField(choices=MEMORY_CHOICES)
    BOOT_DISK_CHOICES = (
        (16, 16),
        (32, 32),
        (64, 64),
        (128, 128)
    )
    boot_disk = models.IntegerField(choices=BOOT_DISK_CHOICES)
    readonly_fields = ('vm_group_id', 'name', 'vmid', 'ip', 'cloud_provider', 'cores', 'sockets', 'memory', 'boot_disk')

    def __str__(self):
        return f'id: {self.id}, vm_group_id: {self.vm_group.id} name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, ' \
               f'cloud_provider: {self.cloud_provider}, cores: {self.cores}, sockets: {self.sockets}, ' \
               f'memory: {self.memory}, boot_disk: {self.boot_disk} '
