from rest_framework import serializers

from ..models.vm_from_img import VmFromImage


class VmFromImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmFromImage
        fields = ('id', 'name', 'vmid', 'ip', 'cores',
                  'sockets', 'memory', 'boot_disk', 'os_image', 'disk_type')
