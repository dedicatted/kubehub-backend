from django.db import models

from kubehub.models.vm import VM
from kubehub.models.os_image import OsImage
from kubehub.models.proxmox_vm_group import ProxmoxVmGroup


class VmFromImage(VM):
    vmid = models.IntegerField()
    os_image = models.ForeignKey(
        to=OsImage,
        on_delete=models.PROTECT,
        related_name='image_based_vms',
        default=0
    )
    vm_group = models.ForeignKey(
        ProxmoxVmGroup,
        on_delete=models.CASCADE,
        related_name="image_vms",
        default=None,
        null=True
    )
    readonly_fields = ('vmid', 'os_image', 'vm_group')

    def __str__(self):
        return f'id: {self.id}, vmid: {self.vmid}, os_image: {self.os_image}, vm_group_id: {self.vm_group.id}'


