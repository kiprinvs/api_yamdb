from datetime import datetime

from rest_framework.exceptions import ValidationError


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError('Год не может быть более текущего')
