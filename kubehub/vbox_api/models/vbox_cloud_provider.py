from django.db import models
from subprocess import check_output

from kubehub.models.cloud_provider import CloudProvider


class VirtualBoxCloudProvider(CloudProvider):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    image_folder = models.CharField(
        max_length=name_max,
        unique=True,
        null=False
    )
    machine_folder = models.CharField(
        max_length=name_max,
        unique=False,
        null=False
    )

    def __str__(self):
        return f'id: {self.id}, image_folder: {self.image_folder}, machine_folder: {self.machine_folder},'

