from rest_framework.permissions import BasePermission, SAFE_METHODS

from shops.models import Shop


class IsAuthenticatedOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or hasattr(obj, 'user') and request.user == obj.user:
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.method in SAFE_METHODS or request.user.is_staff
        )


class IsShopOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if hasattr(obj, 'shop') and hasattr(obj.shop, 'user') and request.user == obj.shop.user:
            return True
        if hasattr(obj, 'user') and request.user == obj.user:
            return True
        if hasattr(obj, 'category') and \
                hasattr(obj.category, 'shop') and \
                hasattr(obj.category.shop, 'user') and \
                request.user == obj.category.shop.user:
            return True
        return False


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated
