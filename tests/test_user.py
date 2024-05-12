import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_register_user(api_client, user_data):
    url = reverse('user-register')
    response = api_client.post(url, user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username=user_data['username']).exists()


@pytest.mark.django_db
def test_login_user(api_client, db, create_user, user_data):
    url = reverse('user-login')
    response = api_client.post(url, user_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.data


@pytest.mark.django_db
def test_login_with_invalid_credentials(api_client):
    url = reverse('user-login')
    data = {'username': 'invalid-user', 'password': 'invalid-password'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == 'Invalid credentials'


@pytest.mark.django_db
def test_login_serializer_invalid(api_client):
    url = reverse('user-login')
    data = {'username': 'test-user'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
