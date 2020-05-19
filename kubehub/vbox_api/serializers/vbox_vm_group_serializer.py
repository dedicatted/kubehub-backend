from rest_framework import serializers

from kubehub.vbox_api.models.vbox_vmg import VboxVmGroup
from kubehub.vbox_api.models.vbox_vm import VirtualBoxVm
from kubehub.vbox_api.serializers.vbox_vm_serializer import VboxVmSerializer


class VboxVmGroupSerializer(serializers.ModelSerializer):
    vbox_vms = VboxVmSerializer(many=True)

    class Meta:
        model = VboxVmGroup
        fields = ('id', 'name', 'user_id', 'status', 'cloud_provider', 'vbox_vms')

    def create(self, validated_data):
        vbox_vms = validated_data.pop('vbox_vms')
        vm_group = VboxVmGroup.objects.create(**validated_data)
        for vm in vbox_vms:
            VirtualBoxVm.objects.create(vm_group=vm_group, **vm)
        return vm_group

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.vbox_vms.set = validated_data.get('vbox_vms', instance.vbox_vms)
        instance.save()

        return instance
