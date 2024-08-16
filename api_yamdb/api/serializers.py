import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from review.models import Category, Genre, Title, GenreTitle
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True, required=False)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def validate(self, data):
        if "year" in data:
            if datetime.datetime.now().year < data["year"]:
                raise ValidationError('Год публикации произведения не может быть больше текущего!')
        return data

    def create(self, validated_data):
        data_dict = {**validated_data}
        data_dict["category"] = get_object_or_404(
            Category.objects, slug=self.initial_data["category"]
        )
        title = Title.objects.create(**data_dict)
        genre_list = self.initial_data.getlist("genre")
        for genre in genre_list:
            current_genre = get_object_or_404(Genre.objects, slug=genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title
