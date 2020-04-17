from django.db import models

from ..models.vm import VM
from ..models.os_image import OsImage


class VmFromImage(VM):
    os_image = models.ForeignKey(
        to=OsImage,
        on_delete=models.PROTECT,
        related_name='vms',
        default=0
    )
    readonly_fields = 'os_image'

    def __str__(self):
        return f'id: {self.id}, os_image: {self.os_image}'


