import pytest
from faker import Faker
from rest_framework.reverse import reverse

from users.models import User
from users.serializers import UserModelSerializer

fake = Faker()


@pytest.mark.django_db
class TestUserAPIView:
    @pytest.fixture
    def users(self):
        data = {
            'username': 'Jack',
            'password': 'string123',
            'email': 'johndoe@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        c = User.objects.create(**data)
        # c.set_password(data['password'])
        return c

    def test_user_model(self, users):
        count = User.objects.count()

        for _ in range(10):
            first_name = fake.unique.first_name()
            last_name = fake.unique.last_name()
            username = fake.profile(fields=['username'])['username']
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=f'{first_name}.{last_name}@{fake.domain_name()}'
            )
            assert first_name == user.first_name
            assert last_name == user.last_name
            assert username == user.username
        assert count < User.objects.count()

    def test_user_create_api(self, client):
        url = reverse('v1:users:register')
        data = {
            'username': 'Jack',
            'password': 'string123',
            'password2': 'string123',
            'email': 'johndoe@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post(url, data=data)
        assert response.status_code == 201
        assert response.json()['username'] == data['username']

    def test_user_retrieve_api(self, client, users):
        url = reverse('v1:users:user-detail', args=(users.id,))
        response = client.get(url)
        assert response.status_code == 200
        # assert response.json() == UserModelSerializer(users).data
        assert sorted(response.json().items()) == sorted(UserModelSerializer(users).data.items())

    def test_user_update_api(self, client, users):
        url = reverse('v1:users:user-detail', args=(users.id,))
        data = {
            'username': 'Jane',
            'email': 'janedoe@example.com',
            'first_name': 'Jane',
        }
        response = client.patch(url, data=data, content_type='application/json')
        assert response.status_code == 200
        response = response.json()
        assert response['first_name'] == data['first_name']
        assert response['username'] == data['username']
        assert response['email'] == data['email']
