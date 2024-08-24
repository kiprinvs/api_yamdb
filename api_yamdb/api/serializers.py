from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME
from users.validators import username_validator

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description',
                  'genre', 'category')

    def to_representation(self, title):
        return TitleGetSerializer(title).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')

        if (
            request
            and request.method == 'POST'
            and Review.objects.filter(
                author=request.user,
                title_id=self.context.get('view').kwargs.get('title_id')
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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
