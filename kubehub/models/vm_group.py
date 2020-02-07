from django.db import models
import subprocess


class VMGroup(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    vm_group_name = models.CharField(max_length=name_max)
    user_id = models.CharField(max_length=name_max)
    vmid = models.CharField(max_length=name_max)
    vm_ip = models.CharField(max_length=name_max)
    cloud_provider_id = models.CharField(max_length=name_max)
    template_id = models.CharField(max_length=name_max)
    readonly_fields = ('user_id', 'vmid', 'vm_ip', 'cloud_provider_id', 'template_id')

    def __str__(self):
        return f'id: {self.id}, vm_group_name: {self.vm_group_name}, user_id: {self.user_id}, vmid: {self.vmid}, ' \
               f'vm_ip: {self.vm_ip}, cloud_provider_id: {self.cloud_provider_id}, template_id: {self.template_id}'
