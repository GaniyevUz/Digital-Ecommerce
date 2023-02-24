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
        # shop = Shop.objects.get(pk=request.parser_context.get('kwargs').get('shop'))
        # return self.has_object_permission(request, view, shop)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or hasattr(obj, 'user') and request.user and request.user == obj.user:
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
