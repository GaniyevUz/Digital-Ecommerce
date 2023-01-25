from shops.models import Category


def collect_shops_categories() -> None:
    categories = (
        "Clothing",
        "Electronics",
        "Books, Movies,  Music and Games",
        "Cosmetics",
        "Bags and Accessories",
        "food",
        "Appliances",
        "Furniture and Household Goods",
        "Sport and Leisure",
        "Toys and Baby Products",
        "Stationery",
        "Garden & Pets",
        "Other"
    )
    for category in categories:
        obj = Category.objects.create(name=category)
        print(f"<Category object: id={obj.pk}, name={obj.name}>")
