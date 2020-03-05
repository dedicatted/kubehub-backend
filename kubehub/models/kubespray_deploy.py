from django.db import models

import subprocess


class KubesprayDeploy(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    statuses = (
        ('deploying', 'deploying'),
        ('successful', 'successful'),
        ('failed', 'failed')
    )
    status = models.CharField(max_length=name_max, choices=statuses)
    log_file_path = models.CharField(max_length=name_max)
    readonly_fields = 'log_file_path'

    def __str__(self):
        return f'id: {self.id}, status: {self.status}, log_file_path: {self.log_file_path}'

