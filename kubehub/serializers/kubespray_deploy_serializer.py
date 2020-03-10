from rest_framework import serializers

from ..models.kubespray_deploy import KubesprayDeploy


class KubesprayDeploySerializer(serializers.ModelSerializer):
    class Meta:
        model = KubesprayDeploy
        fields = ('id', 'status', 'vm_group', 'k8s_cluster')
