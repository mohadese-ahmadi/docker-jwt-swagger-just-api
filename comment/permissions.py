from rest_framework import permissions


class IsAuthorOrSuperOrReadOnly(permissions.BasePermission):
    """اجازه فقط برای نویسنده و سوپر یوزر در متدهای ویرایش/حذف."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.user == request.user
                or request.user.is_superuser)
