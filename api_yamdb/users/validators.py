from django.conf import settings
from django.core.exceptions import ValidationError

def username_validator(value):
    if value in settings.BAD_USERNAMES:
        raise ValidationError(f'Недопустимое имя - {value}')
    return value
