from django.db import models
from subprocess import check_output


class VMGroup(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.IntegerField()
    readonly_fields = ('name', 'user_id')
    statuses = (
        ('creating', 'creating'),
        ('running', 'running'),
        ('removing', 'removing'),
        ('removed', 'removed'),
        ('error', 'error')
    )
    status = models.CharField(max_length=name_max, choices=statuses)

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, user_id: {self.user_id}, status: {self.status}'




