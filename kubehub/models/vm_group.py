from django.db import models
from subprocess import check_output

from ..models.proxmox_cloud_provider import ProxmoxCloudProvider


class VMGroup(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.IntegerField()
    cloud_provider = models.ForeignKey(
        ProxmoxCloudProvider,
        on_delete=models.PROTECT,
        related_name="vms",
        null=True,
        default=None
    )
    statuses = (
        ('creating', 'creating'),
        ('running', 'running'),
        ('removing', 'removing'),
        ('removed', 'removed'),
        ('error', 'error')
    )
    status = models.CharField(max_length=name_max, choices=statuses)
    readonly_fields = ('name', 'user_id', 'cloud_provider')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, user_id: {self.user_id}, status: {self.status},' \
               f'cloud_provider: {self.cloud_provider}'




