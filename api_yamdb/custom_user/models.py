from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME
from .validators import username_me_validator


class CustomUser(AbstractUser):
    """Модель пользователя."""

    class RoleForUsers(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

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
        max_length=MAX_LENGTH_NAME,
        verbose_name='Роль',
        choices=RoleForUsers.choices,
        default=RoleForUsers.USER,
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == self.RoleForUsers.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.RoleForUsers.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            ),
        ]
