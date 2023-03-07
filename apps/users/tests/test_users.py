import pytest
from django_hosts import reverse

from shared.django import TestFixtures
from users.models import User
from users.serializers import UserModelSerializer


@pytest.mark.django_db
class TestUserAPIView(TestFixtures):
    def test_user_model(self, faker, obj_user):
        users_count = User.objects.count()
        self.baker.make(
            'users.User',
            _quantity=10,
            first_name=self.repeat(faker.first_name, 10),
            last_name=self.repeat(faker.last_name, 10),
            email=self.repeat(faker.unique.email, 10)
        )
        assert User.objects.count() == users_count + 10

    def test_user_create_api(self, client):
        url = reverse('api:users:user', host='api')
        data = {
            'password': 'string123',
            'confirm_password': 'string123',
            'email': 'johndoe123@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post(url, data=data)
        assert response.status_code == 201
        assert response.json()['email'] == data['email']

    def test_user_retrieve_api(self, client, auth_header, obj_user):
        url = reverse('api:users:user', host='api')
        response = client.get(url, **auth_header)
        assert response.status_code == 200
        # assert response.json() == UserModelSerializer(obj_user).data
        data = UserModelSerializer(obj_user).data
        assert sorted(response.json().items()) == sorted(data.items())

    def test_user_update_api(self, client, auth_header, obj_user):
        url = reverse('api:users:user', host='api')
        data = {
            'email': 'janedoe@example.com',
            'first_name': 'Jane',
        }
        response = client.patch(url, data=data, content_type='application/json', **auth_header)
        assert response.status_code == 200
        response = response.json()
        assert response['first_name'] == data['first_name']
        assert response['email'] == data['email']

    def test_user_change_default_shop_api(self, client, auth_header, obj_shop, obj_user):
        url = reverse('api:users:user', host='api')
        shop = obj_user.shops.first()
        data = {
            'default_shop': shop.pk
        }
        response = client.patch(url, data=data, **auth_header, content_type='application/json')
        assert response.status_code == 200
        assert response.data['default_shop'] == shop.pk

    def test_user_destroy_api(self, client, auth_header, obj_user):
        url = reverse('api:users:user', host='api')
        response = client.delete(url, **auth_header)
        assert response.status_code == 204
        response = client.get(url, **auth_header)
        assert response.status_code == 401
