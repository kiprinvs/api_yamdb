from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from review.models import Review, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAuthorOrReadOnly
from review.validators import validate_unique_review


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
