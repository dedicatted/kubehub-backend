from rest_framework import serializers

from kubehub.models.vm_type import VmType


class VmTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmType
        fields = ('id', 'cores', 'memory', 'boot_disk')

    def create(self, validated_data):
        vm_type = VmType.objects.create(**validated_data)
        return vm_type

    def update(self, instance, validated_data):
        instance.cores = validated_data.get('cores', instance.cores)
        instance.memory = validated_data.get('memory', instance.memory)
        instance.boot_disk = validated_data.get('boot_disk', instance.boot_disk)
        instance.save()
        return instance
