from rest_framework import serializers
from ..models.vm_group import VMGroup


class VMGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMGroup
        fields = ('id', 'vm_group_name', 'vm_ip')

    def create(self, validated_data):
        vm_group = VMGroup.objects.create(**validated_data)
        return vm_group

    def update(self, instance, validated_data):
        instance.vm_group_name = validated_data.get('vm_group_name', instance.vm_group_name)
        # instance.vm_ip = validated_data.get('vm_ip', instance.vm_ip)
        instance.save()
        return instance
