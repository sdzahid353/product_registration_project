import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import connection
from django.conf import settings
from product_registration_app.models import Product


def pytest_configure(config):
    settings.DATABASES["default"]["NAME"] = "test_db.sqlite3"


@pytest.fixture(scope="session", autouse=True)
def create_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('flush', '--noinput')
        call_command('migrate')


@pytest.fixture(scope="session")
def db_cleanup():
    yield

    with connection.cursor() as cursor:
        cursor.execute("DROP DATABASE test_db.sqlite3")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {'username': 'test_user', 'password': 'test_password'}


@pytest.fixture
def create_user(user_data):
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def product_data():
    return {
        'name': 'Test Product',
        'description': 'Test Description',
        'manufacturer': 'Test Manufacturer',
        'serial_number': '123456',
        'date_of_manufacture': '2024-01-01',
        'category': 'Test Category'
    }


@pytest.fixture
def product_data_2():
    return {
        'name': 'Test Product 2',
        'description': 'Test Description 2',
        'manufacturer': 'Test Manufacturer 2',
        'serial_number': '1234567',
        'date_of_manufacture': '2024-05-03',
        'category': 'Test Category 2'
    }


@pytest.fixture
def create_product(api_client, create_user, product_data):
    user = create_user
    api_client.force_authenticate(user=user)
    return Product.objects.create(**product_data)
