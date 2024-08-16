from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        Model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Имя пользователя {value} уже используется'
            )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'email {value} уже используется'
            )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=128,
        required=True,
        validators=(UnicodeUsernameValidator,)
    )
    confirmation_code = serializers.CharField(required=True)
