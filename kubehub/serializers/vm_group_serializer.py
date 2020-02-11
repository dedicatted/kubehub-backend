from rest_framework import serializers
from ..models.vm_group import VMGroup


class VMGroupSerializer(serializers.ModelSerializer):
    vm = serializers.StringRelatedField(many=True)

    class Meta:
        model = VMGroup
        fields = ('id', 'name', 'user_id', 'cloud_provider_id', 'vm')

    def create(self, validated_data):
        vm_group = VMGroup.objects.create(**validated_data)
        return vm_group
