from django.db import models
from subprocess import check_output

from ..models.proxmox_vm_group import ProxmoxVmGroup
from ..models.kubernetes_version import KubernetesVersion


class KubernetesCluster(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(max_length=name_max, unique=True)
    kubernetes_version_id = models.ForeignKey(
        KubernetesVersion,
        on_delete=models.CASCADE
    )
    vm_group = models.OneToOneField(
        ProxmoxVmGroup,
        on_delete=models.CASCADE
    )
    statuses = (
        ('deploying', 'deploying'),
        ('running', 'running'),
        ('removing', 'removing'),
        ('removed', 'removed'),
        ('error', 'error')
    )
    status = models.CharField(max_length=name_max, choices=statuses)

    readonly_fields = 'k8s_version'

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, kubernetes_version_id: {self.kubernetes_version_id}, ' \
               f'vm_group: {self.vm_group}, status: {self.status}'


