from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shops.models import Category, Currency, Shop


# Register your models here.

@admin.register(Category)
class ShopCategory(ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Currency)
class ShopCurrency(ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = (
        'name', 'languages', 'user', 'category', 'currency', 'about_us', 'delivery_types', 'has_terminal',
        'created_at')
    ordering = ('created_at',)
    search_fields = ('name', 'about_us')
    list_filter = ('category', 'currency', 'delivery_types')
