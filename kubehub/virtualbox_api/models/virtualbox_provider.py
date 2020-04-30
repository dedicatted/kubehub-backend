from django.db import models
from subprocess import check_output

from kubehub.models.cloud_provider import CloudProvider


class VirtualBoxCloudProvider(CloudProvider):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    DEBIAN_SUPPORTED_VERSIONS_CHOICES = (
        ('ubuntu-16.04.6-desktop-amd64', 'ubuntu-16.04.6-desktop-amd64'),
        ('ubuntu-18.04.4-desktop-amd64', 'ubuntu-18.04.4-desktop-amd64')
    )
    debian_supported_versions = models.CharField(
        max_length=name_max,
        choices=DEBIAN_SUPPORTED_VERSIONS_CHOICES
    )

    def __str__(self):
        return f'id: {self.id}, debian_supported_versions: {self.debian_supported_versions}, ' \
               # f'os_type: {self.os_type}'
