from django.db import models

import subprocess


class CloudProvider(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    CP_TYPES = (
        ('Proxmox', 'Proxmox'),
        ('AWS', 'AWS'),
        ('GCP', 'GCP')
    )
    cp_type = models.CharField(max_length=name_max, choices=CP_TYPES)
    name = models.CharField(max_length=name_max)
    api_endpoint = models.CharField(max_length=name_max)
    password = models.CharField(max_length=name_max)
    readonly_fields = ('cp_type', 'api_endpoint', 'password')

    def __str__(self):
        return f'cloud_provider_id: {self.id}, name: {self.name}, api_endpoint: {self.api_endpoint}, ' \
               f'password: {self.password}'
