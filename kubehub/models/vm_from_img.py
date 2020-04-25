from django.db import models

from ..models.vm import VM
from ..models.os_image import OsImage
from ..models.vm_group import VMGroup


class VmFromImage(VM):
    os_image = models.ForeignKey(
        to=OsImage,
        on_delete=models.PROTECT,
        related_name='vms',
        default=0
    )
    vm_group = models.ForeignKey(
        VMGroup,
        on_delete=models.CASCADE,
        related_name="image_vms",
        default=None,
        null=True
    )
    readonly_fields = 'os_image'

    def __str__(self):
        return f'id: {self.id}, os_image: {self.os_image}, vm_group_id: {self.vm_group.id}'


