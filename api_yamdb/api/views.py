from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from review.models import Review, Comment, Genre, Category, Title
from api.serializers import (ReviewSerializer, CommentSerializer,
                             GenreSerializer, CategorySerializer,
                             TitleSerializer)
from api.permissions import IsAuthorOrReadOnly, AdminOrReadOnly
from review.validators import validate_unique_review


class GenreViewSet(
    AdminOrReadOnly,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(
    AdminOrReadOnly,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    ordering_fields = ("name", "year")
    http_method_names = ["get", "post", "patch", "delete"]

    # def perform_create(self, serializer):
    #     serializer.save()
        

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        author = request.user
        title_id = request.data.get('title')
        validate_unique_review(author, title_id)
        return super().create(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
