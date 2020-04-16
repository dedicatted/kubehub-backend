from django.db import models
from subprocess import check_output

from ..models.cloud_provider import CloudProvider


class ProxmoxCloudProvider(CloudProvider):
    name_max = int(check_output("getconf NAME_MAX /", shell=True))
    shared_storage_name = models.CharField(max_length=name_max)
    readonly_fields = 'shared_storage_name'

    def __str__(self):
        return f'id: {self.id}, shared_storage_name: {self.shared_storage_name}'

