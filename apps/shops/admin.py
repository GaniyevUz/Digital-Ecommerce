from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shops.models import Shop, Category, Currency, PaymentProvider


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


@admin.register(PaymentProvider)
class PaymentAdmin(ModelAdmin):
    list_display = ('id', 'title')
