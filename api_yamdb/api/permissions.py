from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Класс, который позволяет редактировать объект только его автору.
    Если запрос на чтение – права доступа предоставляются всем.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
