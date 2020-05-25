from rest_framework import serializers

from kubehub.models.vm_type import VmType


class VmTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmType
        fields = ('id', 'platform_type', 'cores', 'memory', 'boot_disk', 'proxmox_image', 'proxmox_template',
                  'vbox_image')

    def create(self, validated_data):
        vm_type = VmType.objects.create(**validated_data)
        if self.validated_data.get('platform_type') == 'VirtualBox':
            validated_data.update({
                'proxmox_image': None,
                'proxmox_template': None
            })
        elif self.validated_data.get('platform_type') == 'Proxmox_image_based':
            validated_data.update({
                'vbox_image': None,
                'proxmox_template': None
            })
        elif self.validated_data.get('platform_type') == 'Proxmox_template_based':
            validated_data.update({
                'vbox_image': None,
                'proxmox_image': None
            })
        return vm_type

    def update(self, instance, validated_data):
        instance.cores = validated_data.get('cores', instance.cores)
        instance.memory = validated_data.get('memory', instance.memory)
        instance.boot_disk = validated_data.get('boot_disk', instance.boot_disk)
        instance.proxmox_image = validated_data.get('proxmox_image', instance.proxmox_image)
        instance.proxmox_template = validated_data.get('proxmox_template', instance.proxmox_template)
        instance.vbox_image = validated_data.get('vbox_image', instance.vbox_image)
        instance.save()
        return instance
