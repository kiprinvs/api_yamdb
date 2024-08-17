from django.contrib.auth import get_user_model
from django.db import models
from .constants import MAX_NAME_LENGTH
from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель публикаций."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name="Название"
    )
    year = models.SmallIntegerField(
        verbose_name="Год", validators=[validate_year]
    )
    description = models.TextField(verbose_name="Описание", default="")
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        blank=True,
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"
        ordering = ("year",)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель многие ко многим, связывает публикации и жанры."""

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name="Жанр"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Произведение"
    )
