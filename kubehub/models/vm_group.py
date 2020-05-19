from django.db import models
from subprocess import check_output


class VmGroup(models.Model):
    class Meta:
        abstract = True
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(max_length=name_max)
    user_id = models.IntegerField()
    statuses = (
        ('creating', 'creating'),
        ('running', 'running'),
        ('removing', 'removing'),
        ('removed', 'removed'),
        ('error', 'error')
    )
    status = models.CharField(max_length=name_max, choices=statuses)
    readonly_fields = 'name'

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, user_id: {self.user_id}, status: {self.status},'


