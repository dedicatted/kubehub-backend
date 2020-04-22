from rest_framework import serializers

from ..models.vm_group import VMGroup
from ..models.vm_from_template import VmFromTemplate
from ..serializers.vm_from_template_serializer import VmFromTemplateSerializer


class VmGroupFromTemplateSerializer(serializers.ModelSerializer):
    template_vms = VmFromTemplateSerializer(many=True)

    class Meta:
        model = VMGroup
        fields = ('id', 'name', 'user_id', 'status', 'cloud_provider', 'template_vms')

    def create(self, validated_data):
        template_vms = validated_data.pop('template_vms')
        vm_group = VMGroup.objects.create(**validated_data)
        for vm in template_vms:
            VmFromTemplate.objects.create(vm_group=vm_group, **vm)
        return vm_group

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.template_vms.set = validated_data.get('template_vms', instance.template_vms)
        instance.save()

        return instance
