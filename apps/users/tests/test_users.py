import random

import pytest
from faker import Faker
from rest_framework.reverse import reverse

from users.models import User

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
        url = reverse('register')
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
