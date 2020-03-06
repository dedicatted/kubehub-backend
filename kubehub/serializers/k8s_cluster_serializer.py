from rest_framework import serializers

from ..models.k8s_cluster import KubernetesCluster


class KubernetesClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesCluster
        fields = ('id', 'name', 'k8s_version', 'vm_group')

    def create(self, validated_data):
        kubernetes_cluster = KubernetesCluster.objects.create(**validated_data)
        return kubernetes_cluster

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance
