import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from custom_user.models import CustomUser
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

DATA_PATH = os.path.join(
    settings.BASE_DIR, 'static', 'data'
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.import_users()
        self.import_categories()
        self.import_genres()
        self.import_titles()
        self.import_genre_titles()
        self.import_reviews()
        self.import_comments()
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
                category = Category.objects.get(id=row['category'])
                Title.objects.create(
                    id=row['id'], name=row['name'],
                    year=row['year'], category=category
                )

    def import_genre_titles(self):
        with open(
            os.path.join(DATA_PATH, 'genre_title.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    GenreTitle.objects.create(
                        id=row['id'], title=title, genre=genre
                    )
                except Title.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Произведение с id={row['title_id']} не существует."
                        )
                    )
                except Genre.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Жанр с id={row['genre_id']} не существует."
                        )
                    )

    def import_reviews(self):
        with open(
            os.path.join(DATA_PATH, 'review.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    author = CustomUser.objects.get(id=row['author'])
                    Review.objects.create(
                        id=row['id'], title=title, text=row['text'],
                        author=author, score=row['score'],
                        pub_date=row['pub_date']
                    )
                except CustomUser.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Пользователь с id={row['author']} не существует."
                        )
                    )
                except Title.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Произведение с id={row['title_id']} не существует."
                        )
                    )

    def import_comments(self):
        with open(
            os.path.join(DATA_PATH, 'comments.csv'), encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    review = Review.objects.get(id=row['review_id'])
                    author = CustomUser.objects.get(id=row['author'])
                    Comment.objects.create(
                        id=row['id'], review=review, text=row['text'],
                        author=author, pub_date=row['pub_date']
                    )
                except CustomUser.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Пользователь с id={row['author']} не существует."
                        )
                    )
                except Review.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Отзыв с id={row['review_id']} не существует."
                        )
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
