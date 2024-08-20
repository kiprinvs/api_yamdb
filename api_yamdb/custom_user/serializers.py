from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME
from .validators import username_me_validator

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
        validators=(username_me_validator, UnicodeUsernameValidator()),
    )

    def validate(self, data):
        username = User.objects.filter(username=data['username']).exists()
        email = User.objects.filter(email=data['email']).exists()
        if username and not email:
            raise serializers.ValidationError(
                f'email {email} уже используется')
        elif not username and email:
            raise serializers.ValidationError(
                f'Имя пользователя {username} уже используется')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        required=True,
        validators=(UnicodeUsernameValidator,)
    )
    confirmation_code = serializers.CharField()
