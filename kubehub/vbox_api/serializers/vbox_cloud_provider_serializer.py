from rest_framework import serializers

from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider


class VirtualBoxCloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualBoxCloudProvider
        fields = ('id', 'cp_type', 'name', 'api_endpoint', 'password', 'image_folder')

    def create(self, validated_data):
        vbox_cloud_provider = VirtualBoxCloudProvider.objects.create(**validated_data)
        if self.validated_data.get('cp_type') == 'VirtualBox':
            validated_data.update({
                'password': None,
                'api_endpoint': None
            })
        return vbox_cloud_provider

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image_folder = validated_data.get('image_folder', instance.image_folder)
        instance.save()

        return instance

