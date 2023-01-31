from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from parler.admin import TranslatableAdmin

from products.models import Product, Category


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    list_display = 'tree_actions', 'name', 'description'
    list_display_links = 'name',


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name',
