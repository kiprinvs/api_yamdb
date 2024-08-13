from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH_CHAR_FIELD = 128


class CustomUser(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'Admin',
    MODERATOR = 'Moderator',
    USER = 'user'

    class RoleForUsers(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        MODERATOR = 'MODERATOR', 'moderator'
        USER = 'USER', 'user'

    username = models.CharField(
        max_length=MAX_LENGTH_CHAR_FIELD,
        unique=True,
        verbose_name='Отображаемое имя',
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_CHAR_FIELD,
        verbose_name='Почта',
        unique=True,
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_CHAR_FIELD,
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_CHAR_FIELD,
        verbose_name='Фамилия',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=32,
        verbose_name='Роль',
        choices=RoleForUsers.choices,
        default=RoleForUsers.USER,
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',
        ordering = ('id',)

    def __str__(self):
        return self.username
