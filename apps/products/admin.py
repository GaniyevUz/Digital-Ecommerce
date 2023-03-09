from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from products.models import Product, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = 'tree_actions', 'english', 'russian', 'uzbek'
    list_display_links = 'english', 'russian', 'uzbek'

    @staticmethod
    def english(obj):
        if hasattr(obj.name, 'get'):
            return obj.name.get('en')
        return obj.name

    @staticmethod
    def russian(obj):
        if hasattr(obj.name, 'get'):
            return obj.name.get('ru')
        return obj.name

    @staticmethod
    def uzbek(obj):
        if hasattr(obj.name, 'get'):
            return obj.name.get('uz')
        return obj.name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name',
