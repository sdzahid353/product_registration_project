import pytest
from django.urls import reverse
from rest_framework import status
from product_registration_app.models import Product


@pytest.mark.django_db
def test_product_registration(api_client, product_data):
    url = reverse('product-registration')
    response = api_client.post(url, product_data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_product_registration_invalid_data(api_client, create_user, product_data):
    user = create_user
    api_client.force_authenticate(user=user)
    url = reverse('product-registration')

    product_data["date_of_manufacture"] = '2025-01-01'
    invalid_data = product_data

    response = api_client.post(url, invalid_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    expected_errors = [
        "date_of_manufacture: Manufacture date cannot be in the future"
    ]
    assert response.data == {"errors": expected_errors}


@pytest.mark.django_db
def test_authenticated_product_registration(api_client, create_user, product_data):
    user = create_user
    api_client.force_authenticate(user=user)
    url = reverse('product-registration')
    response = api_client.post(url, product_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.filter(name=product_data['name']).exists()


@pytest.mark.django_db
def test_get_queryset_with_query_params(api_client, create_user, product_data, product_data_2):

    user = create_user
    api_client.force_authenticate(user=user)
    product_registration_url = reverse('product-registration')
    product_list_url = reverse('product-list')

    post_product_data_1 = api_client.post(product_registration_url, product_data, format='json')
    post_product_data_2 = api_client.post(product_registration_url, product_data_2, format='json')
    params = {'name': 'Test Product', 'manufacturer': 'Test Manufacturer 2', 'category': 'Test Category'}
    response = api_client.get(
        product_list_url + f'?name={params["name"]}&manufacturer={params["manufacturer"]}&category={params["category"]}')
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data.get('results')) == 1


@pytest.mark.django_db
def test_update_product(api_client, create_user, create_product):
    product = create_product
    url = reverse('product-detail', kwargs={'pk': product.pk})
    data = {'name': 'Updated Product'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    assert product.name == 'Updated Product'


@pytest.mark.django_db
def test_validate_update_product_(api_client, create_user, create_product):
    product = create_product
    url = reverse('product-detail', kwargs={'pk': product.pk})
    data = {'manufacturer': 'Updated manufacturer'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    product.refresh_from_db()
    validation_error = {
        "message": "Validation failed"
    }
    print(response.data)
    assert response.data == validation_error


@pytest.mark.django_db
def test_destroy_product(api_client, create_product):
    product = create_product
    url = reverse('product-detail', kwargs={'pk': product.pk})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Product.objects.filter(pk=product.pk).exists()
