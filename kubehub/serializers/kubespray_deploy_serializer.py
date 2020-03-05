from rest_framework import serializers

from ..models.kubespray_deploy import KubesprayDeploy


class KubesprayDeploySerializer(serializers.ModelSerializer):
    class Meta:
        model = KubesprayDeploy
        fields = ('id', 'status', 'log_file_path')

    def create(self, validated_data):
        kubespray_deploy = KubesprayDeploy.objects.create(**validated_data)
        return kubespray_deploy

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


