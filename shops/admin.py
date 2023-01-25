from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shops.models import Category


# Register your models here.

@admin.register(Category)
class ShopCategory(ModelAdmin):
    list_display = ('pk', 'name')
