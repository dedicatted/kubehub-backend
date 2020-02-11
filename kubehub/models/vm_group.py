from django.db import models
import subprocess


class VMGroup(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.IntegerField()
    cloud_provider_id = models.IntegerField()
    readonly_fields = ('name', 'user_id', 'cloud_provider_id')


class VM(models.Model):
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE)
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    ip = models.CharField(max_length=name_max)
    template_id = models.IntegerField()
    readonly_fields = ('name', 'vmid', 'ip', 'template_id')


def __str__(self):
    return f'vm_id: {self.id}, name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, template_id: {self.template_id}'