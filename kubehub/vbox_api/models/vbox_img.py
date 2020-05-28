from django.db import models
from subprocess import check_output


class VirtualBoxImage(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(
        max_length=name_max,
    )
    img_full_path = models.CharField(
        max_length=name_max,
        unique=True
    )

    readonly_fields = ('img_name', 'img_full_path')

    def __str__(self):
        return f'id: {self.id}, img_name: {self.name}, img_full_path: {self.img_full_path} '
