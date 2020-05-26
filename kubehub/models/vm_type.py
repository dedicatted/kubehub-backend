from django.db import models


class VmType(models.Model):
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

    readonly_fields = ('cores', 'memory', 'boot_disk')

    def __str__(self):
        return f'id: {self.id}, cores: {self.cores}, memory: {self.memory}, boot_disk: {self.boot_disk}'

