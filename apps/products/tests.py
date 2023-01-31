import pytest
from rest_framework.reverse import reverse_lazy, reverse

from products.models import Product
from shops.models import Category


@pytest.mark.django_db
class TestCategoryAPIView:

    @pytest.fixture
    def create_category(self):
        # category = Product.objects.create(name='Category 1')
        # return category
        pass

    def test_product_create_model(self):
        # model
        name = 'Category 2'
        description = 'About Category 2'
        categor = Category.objects.create(name=name)
        price = 1234

        count = Product.objects.count()
        category = Product.objects.create(name=name, description=description, category=categor, price=price)
        assert category.name == name
        assert Product.objects.count() - 1 == count

    def test_product_crud_url(self):  # url
        url_list = reverse_lazy('product-list')
        url_create = reverse_lazy('product-detail', kwargs={'pk': 1})
        assert url_list == '/api/v1/product/'
        assert url_create == '/api/v1/product/1/'

    # def test_product_create_api_view(self, client):  # view
    #     url = reverse('product-list')
    #     data = {
    #         'name': 'Category-2'
    #     }
    #     response = client.post(url, data)
    #     assert response.status_code == 201
    #     assert response.json()['name'] == data['name']

    # def test_category_retrieve_api_view(self, client, categories):  # view
    #     url = reverse('category_retrieve', args=(1,))
    #     response = client.get(url)
    #     assert response.status_code == 200
    #     assert response.json()['name'] == categories.name

    # @pytest.fixture
    # def adverts(self):
    #     fake = Faker()
    #     advert = baker.make(
    #         Advert,
    #         type=fake.random.choice(Advert.Type.choices),
    #         name=fake.name(),
    #         full_name=fake.full_name(),
    #     )
    #     return advert
    #
    # def test_advert_list(self, client):
    #     url = reverse_lazy('adverts:advert-advert')
    #     response = client.get(url)
    #     assert response.status_code == 200
    #
    # def test_advert_create_api(self, client, url):
    #     url = ''
    #     data = {}
    #     response = client.post(url)
    #     assert response.status_code == 201

#         data = {
#             "make": "Ford",
#             "model": "Fiesta",
#             "year": 2020,
#             "vin": "LA32878",
#             "licence": "12345678",
#             "serial": "12345678",
#             'length': 21,
#             'height': 21,
#         }
#         response = client.post(url, data)
#         assert response.status_code == 201

#
# # from tests.auth import AuthMixin
#
#
# @pytest.mark.django_db
# class TestTrailersAPIView:
#     @pytest.fixture
#     def url(self):
#         return reverse('web_api_v1:trailers-list')
#
#     @pytest.fixture
#     def trailers(self) -> Optional[list]:
#         fake = Faker()
#         truck = baker.make(
#             "trucks.Truck",
#             vin=fake.random_number(digits=17),
#             odometer=fake.random_int(min=0, max=1000000),
#             make=fake.random_element(elements=["Ford", "Chevrolet", "Toyota"]),
#             model=fake.random_element(elements=["Fiesta", "Corvette", "Camry"]),
#             year=fake.random_int(min=2000, max=2020),
#             licence=fake.random_number(digits=8),
#             serial=fake.random_number(digits=8),
#         )
#
#         data = baker.make(
#             "trucks.Trailer",
#             truck=truck,
#             make=cycle(("Ford", "Chevrolet", "Toyota")),
#             model=cycle(("Fiesta", "Corvette", "Camry")),
#             year=fake.random_int(min=2000, max=2020),
#             licence=fake.random_number(digits=8),
#             serial=fake.random_number(digits=8),
#             _quantity=10
#         )
#         return data
#
#     def test_create(self, client, url):
#         data = {
#             "make": "Ford",
#             "model": "Fiesta",
#             "year": 2020,
#             "vin": "LA32878",
#             "licence": "12345678",
#             "serial": "12345678",
#             'length': 21,
#             'height': 21,
#         }
#         response = client.post(url, data)
#         assert response.status_code == 201
#
#     def test_get_list(self, client, url, trailers):
#         response = client.get(url)
#         assert response.status_code == 200
#         assert response.data['count'] == len(trailers)
#
#     def test_get_detail(self, client, url, trailers):
#         trailer_id = trailers[0].id
#         url = url + f"{trailer_id}/"
#         response = client.get(url)
#         assert response.status_code == 200
#
#     def test_update(self, client, url, trailers):
#         trailer_id = trailers[0].id
#         url = url + f"{trailer_id}/"
#         response = client.put(url, {
#             "make": "Ford",
#             "model": "Fiesta",
#             "year": 2020,
#             "vin": "LA32878",
#             "licence": "12345678",
#             "serial": "12345678",
#             'length': 21,
#             'height': 21,
#         })
#         assert response.status_code == 200
#
#     def test_delete(self, client, url, trailers):
#         trailer_id = trailers[0].id
#         url = url + f"{trailer_id}/"
#         response = client.delete(url)
#         assert response.status_code == 204
