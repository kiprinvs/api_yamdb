from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME
from .validators import username_validator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSignupSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL, required=True)
    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        required=True,
        validators=(username_validator, UnicodeUsernameValidator()),
    )

    def validate(self, data):
        user_by_email = User.objects.filter(
            email=data['email']
        ).first()
        user_by_username = User.objects.filter(
            username=data['username']
        ).first()
        if user_by_email != user_by_username:
            error_msg = {}
            if user_by_email is not None:
                error_msg['email'] = (
                    'Пользователь с таким email уже существует.'
                )
            if user_by_username is not None:
                error_msg['username'] = (
                    'Пользователь с таким username уже существует.'
                )
            raise serializers.ValidationError(error_msg)
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        required=True,
        validators=(username_validator, UnicodeUsernameValidator())
    )
    confirmation_code = serializers.CharField()
