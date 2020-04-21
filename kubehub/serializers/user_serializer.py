from rest_framework import serializers

from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)

        instance.save()

        return instance




