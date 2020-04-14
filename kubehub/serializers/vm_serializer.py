from rest_framework import serializers

from ..models.vm import VM


class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = ('id', 'name', 'vmid', 'ip', 'cloud_provider', 'cores', 'sockets', 'memory', 'boot_disk')
