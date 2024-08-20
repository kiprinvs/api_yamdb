from rest_framework import viewsets, mixins, filters
from .permissions import AdminOrReadOnly


class CategoryGenreMixin(mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)
    lookup_field = "slug"
