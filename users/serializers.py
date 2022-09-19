from collections import OrderedDict
from rest_framework import serializers

from .models import User


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
        password1 = validated_data.get('password1')
        password2 = validated_data.get('password2')
        print(password1)
        if password1 != password2:
            errors = 'Passwords don\'t match.'
            raise serializers.ValidationError({'password': errors})

        if User.objects.filter(username=validated_data.get('username')).exists():
            msg = 'User with that nickname exists.'
            raise serializers.ValidationError({'password': msg})

        if not any(not el.isnumeric() for el in password1):
            msg = 'Password must contain at least one letter.'
            raise serializers.ValidationError({'password': msg})
        return validated_data

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['email', 'username', ]
