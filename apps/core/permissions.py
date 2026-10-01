"""
Custom permissions for the Probash Mart API.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Allow read-only access to everyone, write access to admins only."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """Allow access to object owner or admin users."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return hasattr(obj, 'user') and obj.user == request.user


class IsAdminUser(BasePermission):
    """Allow access to admin/staff users only."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
