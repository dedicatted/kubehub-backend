from rest_framework import serializers
from ..models.vm_group import VMGroup


class VMGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMGroup
        fields = ('id', 'name', 'vmid', 'ip', 'cloud_provider_id', 'template_id')

    def create(self, validated_data):
        vm_group = VMGroup.objects.create(**validated_data)
        return vm_group
