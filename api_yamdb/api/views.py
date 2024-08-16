from .permissions import AdminOrReadOnly
from rest_framework import viewsets, mixins
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer
from review.models import Genre, Category, Title
from django.db.models import Avg


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
