import pytest
from faker import Faker
from rest_framework.reverse import reverse

from shared.mixins import TestFixtures
from users.models import User
from users.serializers import UserModelSerializer

fake = Faker()


@pytest.mark.django_db
class TestUserAPIView(TestFixtures):
    def test_user_model(self, faker, obj_user):
        users_count = User.objects.count()
        self.baker.make(
            'users.User',
            _quantity=10,
            first_name=self.repeat(faker.first_name, 10),
            last_name=self.repeat(fake.unique.last_name, 10),
            username=self.repeat(faker.user_name, 10)
        )
        assert User.objects.count() == users_count + 10

    def test_user_create_api(self, client):
        url = reverse('api:users:user')
        data = {
            'username': 'Jack123',
            'password': 'string123',
            'confirm_password': 'string123',
            'email': 'johndoe123@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post(url, data=data)
        assert response.status_code == 201
        assert response.json()['username'] == data['username']

    def test_user_retrieve_api(self, client, auth_header, obj_user):
        url = reverse('api:users:user')
        response = client.get(url, **auth_header)
        assert response.status_code == 200
        # assert response.json() == UserModelSerializer(obj_user).data
        data = UserModelSerializer(obj_user).data
        assert sorted(response.json().items()) == sorted(data.items())

    def test_user_update_api(self, client, auth_header, obj_user):
        url = reverse('api:users:user')
        data = {
            'username': 'Jane',
            'email': 'janedoe@example.com',
            'first_name': 'Jane',
        }
        response = client.patch(url, data=data, content_type='application/json', **auth_header)
        assert response.status_code == 200
        response = response.json()
        assert response['first_name'] == data['first_name']
        assert response['username'] == data['username']
        assert response['email'] == data['email']

    def test_user_destroy_api(self, client, auth_header, obj_user):
        url = reverse('api:users:user')
        response = client.delete(url, **auth_header)
        assert response.status_code == 204
        response = client.get(url, **auth_header)
        assert response.status_code == 403

    def test_user_change_default_shop_api(self, client, auth_header, obj_shop, obj_user):
        url = reverse('api:users:user')
        shop = obj_user.shop_set.first()
        data = {
            'default_shop': shop.pk
        }
        response = client.patch(url, data=data, **auth_header, content_type='application/json')
        assert response.status_code == 200
        assert response.data['default_shop'] == shop.pk
