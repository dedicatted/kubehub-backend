from rest_framework import serializers

from kubehub.vbox_api.models.vbox_vm import VirtualBoxVm


class VboxVmSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualBoxVm
        fields = ('id', 'name', 'ip', 'cores', 'memory', 'vbox_os_image')

