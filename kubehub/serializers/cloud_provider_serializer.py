from rest_framework import serializers
from ..models.cloud_provider import CloudProvider


class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = ('id', 'cp_type', 'name', 'api_endpoint', 'password')

    def create(self, validated_data):
        cloud_provider = CloudProvider.objects.create(**validated_data)
        return cloud_provider

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance
