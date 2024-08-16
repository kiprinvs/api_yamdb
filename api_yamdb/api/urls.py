from django.urls import include, path
from rest_framework import routers

from .views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
)

router = routers.DefaultRouter()
router.register(r"titles", TitleViewSet, basename="title")
router.register(r"genres", GenreViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
