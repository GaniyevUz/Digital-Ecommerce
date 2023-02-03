from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from products.models import Product, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = 'tree_actions', 'english', 'russian', 'uzbek'
    list_display_links = 'english', 'russian', 'uzbek'

    @staticmethod
    def english(obj):
        return obj.name.get('en')

    @staticmethod
    def russian(obj):
        return obj.name.get('ru')

    @staticmethod
    def uzbek(obj):
        return obj.name.get('uz')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name',
