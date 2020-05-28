from rest_framework import serializers

from kubehub.models.vm_from_img import VmFromImage


class VmFromImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmFromImage
        fields = ('id', 'name', 'vmid', 'ip', 'os_image', 'cores', 'vm_group', 'memory', 'boot_disk', 'node_type')
