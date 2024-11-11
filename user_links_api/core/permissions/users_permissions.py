from rest_framework import permissions

from apps.users.models import User


def is_active(request):
    return request.user.status == User.ACTIVE


def is_admin(request):
    return request.user.role == User.ADMIN


def is_user(request):
    return request.user.role == User.USER


class IsActive(permissions.BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return request.user and not request.user.is_anonymous and is_active(request)


class IsAdminPermission(permissions.BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return request.user and not request.user.is_anonymous and not request.user.is_superuser and is_admin(request)


class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to super admins.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
