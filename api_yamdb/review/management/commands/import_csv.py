import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from review.models import Category, Genre, Title, Review, Comment
from custom_user.models import CustomUser

DATA_PATH = os.path.join(
    settings.BASE_DIR, 'api_yamdb', 'static', 'data'
)


class Command(BaseCommand):
   
   def handle(self, *args, **kwargs):
        self.import_categories()
        self.import_genres()
        self.import_titles()
        self.import_reviews()
        self.import_comments()
        self.import_users()
        self.stdout.write('Данные были успешно загружены')

    def import_categories(self):
        with open(
            os.path.join(DATA_PATH, 'category.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )

    def import_genres(self):
        with open(
            os.path.join(DATA_PATH, 'genre.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genre.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )

    def import_titles(self):
        with open(
            os.path.join(DATA_PATH, 'titles.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = Category.objects.get(
                    id=row['category']
                )
                Title.objects.create(
                    id=row['id'], name=row['name'],
                    year=row['year'], category=category
                )

    def import_reviews(self):
        with open(
            os.path.join(DATA_PATH, 'review.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                author = CustomUser.objects.get(id=row['author'])
                Review.objects.create(
                    id=row['id'], title=title, text=row['text'],
                    author=author, score=row['score'],
                    pub_date=row['pub_date']
                )

    def import_comments(self):
        with open(
            os.path.join(DATA_PATH, 'comments.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                review = Review.objects.get(id=row['review_id'])
                author = CustomUser.objects.get(id=row['author'])
                Comment.objects.create(
                    id=row['id'], review=review, text=row['text'],
                    author=author, pub_date=row['pub_date']
                )

    def import_users(self):
        with open(
            os.path.join(DATA_PATH, 'users.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                CustomUser.objects.create(
                    id=row['id'], username=row['username'],
                    email=row['email'], first_name=row['first_name'],
                    last_name=row['last_name'], bio=row['bio'],
                    role=row['role']
                )
