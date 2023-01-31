from django.contrib import admin
from parler.admin import TranslatableAdmin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(TranslatableAdmin):
    list_display = ('first_name', 'status', 'phone')
