from django.db import models

from ..models.vm import VM
from ..models.template import Template


class VmFromTemplate(VM):
    template = models.ForeignKey(Template, on_delete=models.PROTECT, related_name="vms")
    readonly_fields = 'template'

    def __str__(self):
        return f'id: {self.id}, template: {self.template}'

