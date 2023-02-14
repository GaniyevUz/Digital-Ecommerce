from django.db.models import Model, DateTimeField


def category_directory_path(instance, filename):
    return f'shop/{instance.shop.id}categories/{filename}'


def product_directory_path(instance, filename):
    return f'shop/{instance.shop.id}/products/{instance.category.id}/{filename}'

#
# class BaseModel(Model):
#     created_at = DateTimeField(auto_now_add=True, editable=False)
#     updated_at = DateTimeField(auto_now=True, editable=False)
