from rest_framework import serializers

from ..models.virtualbox_provider import VirtualBoxCloudProvider


class VirtualBoxCloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualBoxCloudProvider
        fields = ('id', 'cp_type', 'name', 'api_endpoint', 'password', 'debian_supported_versions')

    def create(self, validated_data):
        if self.validated_data.get('api_endpoint'):
            VirtualBoxCloudProvider.api_endpoint = self.validated_data.get('api_endpoint')
        if self.validated_data.get('password'):
            VirtualBoxCloudProvider.password = self.validated_data.get('password')
        cloud_provider = VirtualBoxCloudProvider.objects.create(**validated_data)
        return cloud_provider

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance

