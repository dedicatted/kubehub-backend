from rest_framework import serializers

from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider


class VirtualBoxCloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualBoxCloudProvider
        fields = ('id', 'cp_type', 'name', 'api_endpoint', 'password', 'vbox_img_dir')

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

