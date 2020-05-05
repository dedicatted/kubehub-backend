from django.db import models
from subprocess import check_output

from kubehub.models.cloud_provider import CloudProvider


class VirtualBoxCloudProvider(CloudProvider):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    vbox_img_dir = models.CharField(
        max_length=name_max,
        unique=True,
        null=False
    )

    def __str__(self):
        return f'id: {self.id}, vbox_img_dir: {self.vbox_img_dir}, '

