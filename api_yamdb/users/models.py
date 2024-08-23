from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import MAX_LENGTH_NAME
from .validators import username_validator


class User(AbstractUser):
    """Модель пользователя."""

    class RoleChoice(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        verbose_name='Имя пользователя',
        validators=(username_validator, UnicodeUsernameValidator()),
    )
    email = models.EmailField(
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
        max_length=MAX_LENGTH_NAME,
        verbose_name='Роль',
        choices=RoleChoice.choices,
        default=RoleChoice.USER,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',
        ordering = ('username', 'role')

    def __str__(self):
        return f'{self.username} - {self.email}'

    @property
    def is_moderator(self):
        return self.role == self.RoleChoice.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.RoleChoice.ADMIN
            or self.is_superuser
        )
