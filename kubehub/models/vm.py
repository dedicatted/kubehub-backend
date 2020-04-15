from django.db import models
from subprocess import check_output

from ..models.cloud_provider import CloudProvider
from ..models.vm_group import VMGroup


class VM(models.Model):
    class Meta:
        abstract = True
    name_max = int(check_output("getconf NAME_MAX /", shell=True))
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE, related_name="vms")
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    ip = models.CharField(max_length=name_max)
    cloud_provider = models.ForeignKey(CloudProvider, on_delete=models.PROTECT, related_name="vms")
    readonly_fields = ('vm_group_id', 'name', 'vmid', 'ip', 'cloud_provider')

    def __str__(self):
        return f'id: {self.id}, vm_group_id: {self.vm_group.id} name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, ' \
               f'cloud_provider: {self.cloud_provider}'
