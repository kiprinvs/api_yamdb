from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSignupSerializer(UserSerializer):

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        try:
            user, _ = User.objects.get_or_create(username=username,
                                                 email=email)
        except IntegrityError:
            if User.objects.filter(username=username).first():
                raise serializers.ValidationError(
                    f'Имя пользователя {username} уже используется'
                )
            else:
                raise serializers.ValidationError(
                    f'email {email} уже используется'
                )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=128,
        required=True,
        validators=(UnicodeUsernameValidator,)
    )
    confirmation_code = serializers.CharField(required=True)
