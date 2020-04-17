from rest_framework import serializers

from ..models.os_image import OsImage


class OsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OsImage
        fields = ('name', 'vmid', 'os_type', 'bios', 'scsi_controller_model', 'storage')

    def create(self, validated_data):
        os_image = OsImage.objects.create(**validated_data)
        return os_image
