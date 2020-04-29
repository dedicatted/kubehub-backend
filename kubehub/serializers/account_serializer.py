from rest_framework import serializers

from ..models.account import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = Account
        fields = ('email', 'username', 'password', 'password2', 'is_admin', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_admin': {'required': False},
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']

        )
        if self.validated_data.get('is_admin'):
            account.is_admin = self.validated_data.get('is_admin')

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)

        instance.save()

        return instance




