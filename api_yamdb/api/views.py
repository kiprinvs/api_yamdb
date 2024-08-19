from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment, Genre, Category, Title
from api.serializers import (ReviewSerializer, CommentSerializer,
                             GenreSerializer, CategorySerializer,
                             TitleSerializer)
from api.permissions import IsAuthorOrModeratorOrReadOnly, AdminOrReadOnly
from reviews.validators import validate_unique_review


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
    # pagination_class = PageNumberPagination

    # def create(self, request, *args, **kwargs):        
    #     return super().create(request, *args, **kwargs)
        

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def create(self, request, *args, **kwargs):
        author = request.user
        title_id = self.kwargs.get('title_id')
        validate_unique_review(author, title_id)
        return super().create(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)
    
    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
