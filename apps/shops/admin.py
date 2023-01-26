from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shops.models import Shop, ShopCategory, ShopCurrency


# Register your models here.

@admin.register(ShopCategory)
class ShopCategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(ShopCurrency)
class ShopCurrencyAdmin(ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = ('name', 'shop_category')
    ordering = ('created_at',)
    search_fields = ('name', 'about_us')
    list_filter = ('shop_category', 'shop_currency')
