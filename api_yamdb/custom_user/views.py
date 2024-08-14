from django.contrib.auth import get_user_model
from rest_framework import filters, pagination, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSingupSerializer, UserSerializer

User = get_user_model()


class SingupView(views.APIView):

    def post(self, request):
        serializer = UserSingupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVIewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False)
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
