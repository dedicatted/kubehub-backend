from django.db import models

import subprocess

from ..models.cloud_provider import CloudProvider


class VMGroup(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.IntegerField()
    readonly_fields = ('name', 'user_id')
    statuses = (
        ('creating', 'creating'),
        ('running', 'running'),
        ('removing', 'removing'),
        ('removed', 'removed'),
        ('error', 'error')
    )
    status = models.CharField(max_length=name_max, choices=statuses)

    def __str__(self):
        return f'vmg_id: {self.id}, name: {self.name}, user_id: {self.user_id}, status: {self.status}'


class VM(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE, related_name="vms")
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    ip = models.CharField(max_length=name_max)
    template_id = models.IntegerField()
    cloud_provider = models.ForeignKey(CloudProvider, on_delete=models.PROTECT, related_name="vms")
    readonly_fields = ('name', 'vmid', 'ip', 'template_id', 'cloud_provider_id')

    def __str__(self):
        return f'vm_id: {self.id}, name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, ' \
               f'template_id: {self.template_id}, cloud_provider: {self.cloud_provider}, ' \
               f'vm_group_id: {self.vm_group.id}'
