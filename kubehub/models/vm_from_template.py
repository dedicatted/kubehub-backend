from django.db import models

from kubehub.models.vm import VM
from kubehub.models.template import Template
from kubehub.models.proxmox_vm_group import ProxmoxVmGroup


class VmFromTemplate(VM):
    vmid = models.IntegerField()
    template = models.ForeignKey(
        to=Template,
        on_delete=models.PROTECT,
        related_name='template_based_vms',
        default=0
    )
    vm_group = models.ForeignKey(
        ProxmoxVmGroup,
        on_delete=models.CASCADE,
        related_name="template_vms",
        default=None
    )
    readonly_fields = ('vmid', 'template', 'vm_group')

    def __str__(self):
        return f'id: {self.id}, vmid: {self.vmid}, template: {self.template}, vm_group_id: {self.vm_group.id}, '

