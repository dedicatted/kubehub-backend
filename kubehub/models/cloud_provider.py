from django.db import models
from subprocess import check_output


class CloudProvider(models.Model):
    class Meta:
        abstract = True
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    CP_TYPES = (
        ('Proxmox', 'Proxmox'),
        ('AWS', 'AWS'),
        ('GCP', 'GCP')
    )
    cp_type = models.CharField(
        max_length=name_max,
        choices=CP_TYPES,
        null=True
    )
    name = models.CharField(
        max_length=name_max,
        unique=True,
        null=True
    )
    api_endpoint = models.CharField(
        max_length=name_max,
        unique=True,
        null=True
    )
    password = models.CharField(
        max_length=name_max,
        unique=True,
        null=True
    )
    readonly_fields = ('cp_type', 'api_endpoint', 'password')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, api_endpoint: {self.api_endpoint}, ' \
               f'password: {self.password}'


