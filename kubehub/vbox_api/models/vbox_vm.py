from django.db import models
from kubehub.models.vm import VM

from kubehub.vbox_api.models.vbox_vmg import VboxVmGroup
from kubehub.vbox_api.models.vbox_img import VirtualBoxImage


class VirtualBoxVm(VM):
    vbox_os_image = models.ForeignKey(
        to=VirtualBoxImage,
        on_delete=models.PROTECT,
        related_name='vbox_image_based_vms',
        default=0
    )
    vm_group = models.ForeignKey(
        VboxVmGroup,
        on_delete=models.CASCADE,
        related_name="vbox_vms",
        default=None,
        null=True
    )
    readonly_fields = 'vbox_os_image'

    def __str__(self):
        return f'id: {self.id}, vbox_os_image: {self.vbox_os_image}, vm_group_id: {self.vm_group.id}'
