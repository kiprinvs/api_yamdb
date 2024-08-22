from django.core.exceptions import ValidationError

from .constants import BAD_USERNAMES


def username_validator(value):
    if value in BAD_USERNAMES:
        raise ValidationError('Недопустимое имя - {value}')
    return value
