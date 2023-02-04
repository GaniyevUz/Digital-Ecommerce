from django.contrib import admin
from django.contrib.admin import ModelAdmin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('first_name', 'status', 'phone')
