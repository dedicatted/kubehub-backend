from django.db import models
from subprocess import check_output

from kubehub.models.cloud_provider import CloudProvider


class VirtualBoxCloudProvider(CloudProvider):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    api_endpoint = models.CharField(
        max_length=name_max,
        null=True
    )
    password = models.CharField(
        max_length=name_max,
        unique=True,
        null=True
    )
    image_folder = models.CharField(
        max_length=name_max,
        null=False
    )

    def __str__(self):
        return f'id: {self.id}, api_endpoint {self.api_endpoint}, password {self.password}, ' \
               f'image_folder: {self.image_folder}'

