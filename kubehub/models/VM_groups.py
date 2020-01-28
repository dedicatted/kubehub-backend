from django.db import models
import subprocess


class VmGroups(models.Model):
    name_max = subprocess.check_output("getconf NAME_MAX /", shell=True)
    vm_group_name = models.CharField(max_length=name_max)
    vm_ip = models.CharField(max_length=name_max)

    def __str__(self):
        return f'id: {self.id}, vm_group_name: {self.vm_group_name}, vm_ip: {self.vm_ip}'
