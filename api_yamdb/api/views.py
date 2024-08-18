from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from django.shortcuts import get_object_or_404
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
    queryset = Title.objects.all()
    # queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    ordering_fields = ("name", "year")
    http_method_names = ["get", "post", "patch", "delete"]

    def create(self, request, *args, **kwargs):        
        return super().create(request, *args, **kwargs)
        

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id) 
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        author = request.user
        title_id = self.kwargs.get('title_id')
        validate_unique_review(author, title_id)
        return super().create(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
