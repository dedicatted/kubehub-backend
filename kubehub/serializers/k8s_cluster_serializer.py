from rest_framework import serializers

from ..models.k8s_cluster import KubernetesCluster


class KubernetesClusterSerializer(serializers.ModelSerializer):

    class Meta:
        model = KubernetesCluster
        fields = ('id', 'name', 'k8s_version', 'vm_group', 'status')

    def create(self, validated_data):
        kubernetes_cluster = KubernetesCluster.objects.create(**validated_data)
        return kubernetes_cluster

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.name = validated_data.get('name', instance.name)
        instance.kubespray_deployments.set = validated_data.get('kubespray_deployments', instance.kubespray_deployments)
        instance.save()

        return instance
