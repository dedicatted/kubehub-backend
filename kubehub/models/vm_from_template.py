from django.db import models
from subprocess import check_output


from kubehub.models.vm import VM
from kubehub.models.template import Template
from kubehub.models.proxmox_vm_group import ProxmoxVmGroup


class VmFromTemplate(VM):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
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
    readonly_fields = ('vmid', 'template', 'vm_group', 'memory')

    def __str__(self):
        return f'id: {self.id}, vmid: {self.vmid}, template: {self.template}, vm_group_id: {self.vm_group.id}, ' \
               f'memory {self.memory}'

