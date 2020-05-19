from rest_framework import serializers

from ..models.proxmox_vm_group import ProxmoxVmGroup
from ..models.vm_from_img import VmFromImage
from ..serializers.vm_from_img_serializer import VmFromImageSerializer


class VmGroupFromImageSerializer(serializers.ModelSerializer):
    image_vms = VmFromImageSerializer(many=True)

    class Meta:
        model = ProxmoxVmGroup
        fields = ('id', 'name', 'user_id', 'status', 'cloud_provider', 'image_vms')

    def create(self, validated_data):
        image_vms = validated_data.pop('image_vms')
        vm_group = ProxmoxVmGroup.objects.create(**validated_data)
        for vm in image_vms:
            VmFromImage.objects.create(vm_group=vm_group, **vm)
        return vm_group

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.image_vms.set = validated_data.get('image_vms', instance.image_vms)
        instance.save()

        return instance
