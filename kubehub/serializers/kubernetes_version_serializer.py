from rest_framework import serializers

from ..models.kubernetes_version import KubernetesVersion


class KubernetesVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesVersion
        fields = ('id', 'version')

    def create(self, validated_data):
        kubernetes_version = KubernetesVersion.objects.create(**validated_data)
        return kubernetes_version

