from rest_framework import serializers


def validate_password(validated_data):
    password1 = validated_data.get('password1')
    password2 = validated_data.get('password2')

    if password1 != password2:
        errors = 'Passwords don\'t match.'
        raise serializers.ValidationError({'password': errors})

    if not any(not el.isnumeric() for el in password1):
        msg = 'Password must contain at least one letter.'
        raise serializers.ValidationError({'password': msg})

    return validated_data
