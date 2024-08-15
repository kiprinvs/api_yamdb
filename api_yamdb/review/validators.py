from datetime import datetime
from rest_framework.exceptions import ValidationError
from review.models import Review


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError("Год не может быть более текущего")
    

def validate_unique_review(author, title_id):
    if Review.objects.filter(author=author, title_id=title_id).exists():
        raise ValidationError('Вы уже оставили отзыв на это произведение.')
