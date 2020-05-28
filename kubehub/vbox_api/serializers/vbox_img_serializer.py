from rest_framework import serializers

from kubehub.vbox_api.models.vbox_img import VirtualBoxImage


class VirtualBoxImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualBoxImage
        fields = ('id', 'name', 'img_full_path')

    def create(self, validated_data):
        vbox_img = VirtualBoxImage.objects.create(**validated_data)
        return vbox_img
