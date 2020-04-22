from django.db import models

from ..models.vm import VM
from ..models.template import Template
from ..models.vm_group import VMGroup


class VmFromTemplate(VM):
    template = models.ForeignKey(
        to=Template,
        on_delete=models.PROTECT,
        related_name='vms',
        default=0
    )
    vm_group = models.ForeignKey(
        VMGroup,
        on_delete=models.CASCADE,
        related_name="template_vms",
        default=None
    )
    readonly_fields = 'template'

    def __str__(self):
        return f'id: {self.id}, template: {self.template}, vm_group_id: {self.vm_group.id}'


