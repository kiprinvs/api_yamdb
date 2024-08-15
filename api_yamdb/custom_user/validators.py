from django.core.exceptions import ValidationError


def username_me_validator(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя')
    return value
