from django.db import models

import subprocess


class VMGroup(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.IntegerField()
    readonly_fields = ('name', 'user_id')
    status = models.CharField(max_length=name_max)

    def __str__(self):
        return f'vmg_id: {self.id}, name: {self.name}, user_id: {self.user_id}, status: {self.status}'


class VM(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE, related_name="vms")
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    ip = models.CharField(max_length=name_max)
    template_id = models.IntegerField()
    cloud_provider_id = models.IntegerField()

    readonly_fields = ('name', 'vmid', 'ip', 'template_id', 'cloud_provider_id')

    def __str__(self):
        return f'vm_id: {self.id}, name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, ' \
               f'template_id: {self.template_id}, cloud_provider_id: {self.cloud_provider_id}, ' \
               f'vm_group_id: {self.vm_group.id}'
