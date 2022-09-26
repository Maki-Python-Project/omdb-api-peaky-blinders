from collections import OrderedDict
from rest_framework import serializers

from .models import User
from .utils import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        required=True, write_only=True, min_length=8
    )
    password2 = serializers.CharField(
        required=True, write_only=True, min_length=8
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, validated_data: OrderedDict) -> OrderedDict:
        if User.objects.filter(username=validated_data.get('username')).exists():
            msg = 'User with that nickname exists.'
            raise serializers.ValidationError({'password': msg})

        return validate_password(validated_data)

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            msg = 'User with that email exists.'
            raise serializers.ValidationError({'password': msg})
        return email

    def save(self) -> User:
        password1 = self.validated_data.get('password1')
        user = User(
            username=self.validated_data.get('username'),
            email=self.validated_data.get('email')
        )
        user.set_password(password1)
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, min_length=8)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']

    def validate(self, validated_data: OrderedDict) -> OrderedDict:
        return validate_password(validated_data)

    def validate_old_password(self, value):
        user = self.context['request'].user
        print(user)
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data: OrderedDict):

        instance.set_password(validated_data['password1'])
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['email', 'username', ]
