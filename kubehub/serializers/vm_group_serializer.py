from rest_framework import serializers
from ..models.vm_group import VMGroup, VM


class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = ('id', 'name', 'vmid', 'ip', 'template_id', 'cloud_provider_id')


class VMGroupSerializer(serializers.ModelSerializer):
    vms = VMSerializer(many=True)

    class Meta:
        model = VMGroup
        fields = ('id', 'name', 'user_id', 'vms')

    def create(self, validated_data):
        vms = validated_data.pop('vms')
        vm_group = VMGroup.objects.create(**validated_data)
        for vm in vms:
            VM.objects.create(vm_group=vm_group, **vm)
        return vm_group
