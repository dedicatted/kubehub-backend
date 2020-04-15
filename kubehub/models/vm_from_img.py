from django.db import models

from ..models.vm import VM


class VmFromImage(VM):
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
    readonly_fields = ('cores', 'sockets', 'memory', 'boot_disk')

    def __str__(self):
        return f'id: {self.id}, cores: {self.cores}, sockets: {self.sockets}, ' \
               f'memory: {self.memory}, boot_disk: {self.boot_disk}'


