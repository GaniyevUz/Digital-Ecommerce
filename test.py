# from itertools import repeat, cycle
from random import choices, randint

from faker import Faker

fake = Faker()

products = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 22, 23, 525]


def repeat(a, b):
    for i in range(b):
        yield choices(products, k=randint(1, len(products)))


print(list(repeat(fake.unique.user_name, 10)))
