def category_directory_path(instance, filename):
    return f'shop/{instance.shop.id}categories/{filename}'


def product_directory_path(instance, filename):
    return f'shop/{instance.shop.id}/products/{instance.category.id}/{filename}'
