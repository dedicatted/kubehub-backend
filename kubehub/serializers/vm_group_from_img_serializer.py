from rest_framework import serializers

from ..models.vm_group import VMGroup
from ..models.vm_from_img import VmFromImage
from ..serializers.vm_from_img_serializer import VmFromImageSerializer


class VmGroupFromImageSerializer(serializers.ModelSerializer):
    vms = VmFromImageSerializer(many=True)

    class Meta:
        model = VMGroup
        fields = ('id', 'name', 'user_id', 'status', 'vms')

    def create(self, validated_data):
        vms = validated_data.pop('vms')
        vm_group = VMGroup.objects.create(**validated_data)
        for vm in vms:
            VmFromImage.objects.create(vm_group=vm_group, **vm)
        return vm_group

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.vms.set = validated_data.get('vms', instance.vms)
        instance.save()

        return instance