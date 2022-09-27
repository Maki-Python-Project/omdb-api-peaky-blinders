import os

from rest_framework import serializers
from collections import OrderedDict
from django.core.mail import send_mail


def validate_password(validated_data: OrderedDict) -> OrderedDict:
    password1 = validated_data.get('password1')
    password2 = validated_data.get('password2')

    if password1 != password2:
        errors = 'Passwords don\'t match.'
        raise serializers.ValidationError({'password': errors})

    if not any(not el.isnumeric() for el in password1):
        msg = 'Password must contain at least one letter.'
        raise serializers.ValidationError({'password': msg})

    return validated_data


def send(user_email: str, user_name: str) -> None:
    send_mail(
        'You have just registered on our website',
        f'Welcome, {user_name}',
        os.getenv('EMAIL_HOST'),
        [user_email],
        fail_silently=False
    )
