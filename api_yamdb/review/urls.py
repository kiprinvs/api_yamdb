from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(
    'titles/(?P<title_id>[\\d]+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    'titles/(?P<title_id>[\\d]+)/reviews/(?P<review_id>[\\d]+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
