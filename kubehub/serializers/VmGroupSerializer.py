from rest_framework import serializers
from ..models.VmGroup import VmGroups


class VmGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmGroups
        fields = ('id', 'vm_group_name', 'vm_ip')

    def create(self, validated_data):
        vm_groups = VmGroups.objects.create(**validated_data)
        return vm_groups

    def update(self, instance, validated_data):
        instance.vm_group_name = validated_data.get('vm_group_name', instance.vm_group_name)
        instance.vm_ip = validated_data.get('vm_ip', instance.vm_ip)
        instance.save()
        return instance
