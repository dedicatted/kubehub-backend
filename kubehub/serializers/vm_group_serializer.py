from rest_framework import serializers

from ..models.vm_group import VMGroup
from ..models.vm import VM
from ..serializers.vm_serializer import VMSerializer

#
# class VMSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VM
#         fields = ('id', 'name', 'vmid', 'ip', 'template', 'cloud_provider')


class VMGroupSerializer(serializers.ModelSerializer):
    vms = VMSerializer(many=True)

    class Meta:
        model = VMGroup
        fields = ('id', 'name', 'user_id', 'status', 'vms')

    def create(self, validated_data):
        vms = validated_data.pop('vms')
        vm_group = VMGroup.objects.create(**validated_data)
        for vm in vms:
            VM.objects.create(vm_group=vm_group, **vm)
        return vm_group

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.vms.set = validated_data.get('vms', instance.vms)
        instance.save()

        return instance
