from rest_framework import serializers
from ..models.template import Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('name', 'vmid', 'diskread', 'template', 'status', 'disk', 'node', 'cpu', 'diskwrite', 'maxcpu',
                  'type', 'netin', 'maxdisk', 'mem', 'maxmem', 'netout', 'uptime')

    def create(self, validated_data):
        template = Template.objects.create(**validated_data)
        return template
