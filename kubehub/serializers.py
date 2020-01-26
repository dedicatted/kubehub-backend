from rest_framework import serializers
from . models import CloudProvider


class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = ('id', 'cp_type', 'name', 'api_endpoint', 'password')


    def create(self, validated_data):
        cloud_probider = CloudProvider.objects.create(**validated_data)
        return cloud_probider


    def update(self, instance,validated_data):
        instance.cp_type = validated_data.get('cp_type', instance.cp_type)
        instance.name = validated_data.get('name', instance.name)
        instance.api_endpoint = validated_data.get('api_endpoint', instance.api_endpoint)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        return instance