from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shops.models import Shop, Category, Currency


# Register your models here.

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = ('name', 'shop_category')
    ordering = ('created_at',)
    search_fields = ('name', 'about_us')
    list_filter = ('shop_category', 'shop_currency')
