from django.db import models
from subprocess import check_output


class KubernetesVersion(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    VERSIONS = (
        ('v1.14.6', 'v1.14.6'),
        ('v1.15.3', 'v1.15.3'),
        ('v1.15.8', 'v1.15.8'),
        ('v1.15.11', 'v1.15.11'),
        ('v1.16.8', 'v1.16.8')
    )
    version = models.CharField(max_length=name_max, choices=VERSIONS)
    readonly_fields = 'version'

    def __str__(self):
        return f'id: {self.id}, version: {self.version}'

