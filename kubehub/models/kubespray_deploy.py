from django.db import models
from subprocess import check_output

from ..models.vm_group import VMGroup
from ..models.k8s_cluster import KubernetesCluster


class KubesprayDeploy(models.Model):
    name_max = int(check_output("getconf NAME_MAX /", shell=True))
    k8s_cluster = models.ForeignKey(KubernetesCluster, on_delete=models.CASCADE, related_name="kubespray_deployments")
    statuses = (
        ('deploying', 'deploying'),
        ('successful', 'successful'),
        ('failed', 'failed')
    )
    status = models.CharField(max_length=name_max, choices=statuses)
    vm_group = models.ForeignKey(VMGroup, on_delete=models.CASCADE, related_name="kubespray_deployments")
    readonly_fields = 'vm_group, k8s_cluster_id'

    def __str__(self):
        return f'id: {self.id}, status: {self.status}, vm_group: {self.vm_group}, k8s_cluster_id: {self.k8s_cluster.id}'

