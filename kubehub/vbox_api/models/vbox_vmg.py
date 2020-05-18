from django.db import models

from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider
from kubehub.models.vm_group import VmGroup


class VboxVmGroup(VmGroup):
    cloud_provider = models.ForeignKey(
        VirtualBoxCloudProvider,
        on_delete=models.PROTECT,
        related_name="vms",
        null=True,
        default=None
    )
    readonly_fields = 'cloud_provider'

    def __str__(self):
        return f'id: {self.id}, cloud_provider: {self.cloud_provider}'
