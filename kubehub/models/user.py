from django.db import models
from subprocess import check_output


class User(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    first_name = models.CharField(
        max_length=name_max,
        null=False,
        default=None
    )
    last_name = models.CharField(
        max_length=name_max,
        null=False,
        default=None
    )
    password = models.CharField(
        max_length=name_max,
        null=False,
        default=None
    )
    email = models.EmailField(
        max_length=name_max,
        null=False,
        default=None
    )
    readonly_fields = 'email'

    def __str__(self):
        return f'id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, ' \
               f'password: {self.password}, email: {self.email}'
