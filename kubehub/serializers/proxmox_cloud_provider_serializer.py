from rest_framework import serializers

from ..models.proxmox_cloud_provider import ProxmoxCloudProvider


class ProxmoxCloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxmoxCloudProvider
        fields = ('id', 'cp_type', 'name', 'api_endpoint', 'password', 'shared_storage_name')

    def create(self, validated_data):
        cloud_provider = ProxmoxCloudProvider.objects.create(**validated_data)
        return cloud_provider

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance
