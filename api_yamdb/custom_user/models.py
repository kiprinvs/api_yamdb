from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import username_me_validator

MAX_LENGTH_NAME = 150
MAX_LENGTH_EMAIL = 254


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
        max_length=MAX_LENGTH_NAME,
        unique=True,
        verbose_name='Имя пользователя',
        validators=(username_me_validator, UnicodeUsernameValidator()),
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        verbose_name='Почта',
        unique=True,
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
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

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            ),
        ]
