from django.db import models

from kubehub.models.vm_group import VmGroup
from kubehub.models.proxmox_cloud_provider import ProxmoxCloudProvider


class ProxmoxVmGroup(VmGroup):
    cloud_provider = models.ForeignKey(
        ProxmoxCloudProvider,
        on_delete=models.PROTECT,
        related_name="vms",
        null=True,
        default=None
    )

    def __str__(self):
        return f'id: {self.id}, cloud_provider: {self.cloud_provider}'




