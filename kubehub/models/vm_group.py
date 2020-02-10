from django.db import models
import subprocess


class VMGroup(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.CharField(max_length=name_max)
    vmid = models.CharField(max_length=name_max)
    ip = models.CharField(max_length=name_max)
    cloud_provider_id = models.CharField(max_length=name_max)
    template_id = models.CharField(max_length=name_max)
    readonly_fields = ('vmid', 'ip', 'cloud_provider_id', 'template_id')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, vmid: {self.vmid}, ip: {self.ip}, ' \
               f'cloud_provider_id: {self.cloud_provider_id}, template_id: {self.template_id}'
