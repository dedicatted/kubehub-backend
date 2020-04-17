from rest_framework import serializers

from ..models.vm_from_template import VmFromTemplate


class VmFromTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmFromTemplate
        fields = ('id', 'name', 'vmid', 'ip', 'template', 'cloud_provider', 'cores',
                  'sockets', 'memory', 'boot_disk', 'disk_type')
