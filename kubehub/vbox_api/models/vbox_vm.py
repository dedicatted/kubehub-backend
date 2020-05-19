from django.db import models
from subprocess import check_output

from kubehub.vbox_api.models.vbox_vmg import VboxVmGroup
from kubehub.vbox_api.models.vbox_img import VirtualBoxImage


class VirtualBoxVm(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(max_length=name_max)
    ip = models.CharField(max_length=name_max)
    CORES_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4)
    )
    cores = models.IntegerField(
        choices=CORES_CHOICES,
        default=1
    )
    MEMORY_CHOICES = (
        (1, 1),
        (2, 2),
        (4, 4),
        (8, 8),
        (16, 16)
    )
    memory = models.IntegerField(
        choices=MEMORY_CHOICES,
        default=1
    )

    vbox_os_image = models.ForeignKey(
        to=VirtualBoxImage,
        on_delete=models.PROTECT,
        related_name='vms',
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
