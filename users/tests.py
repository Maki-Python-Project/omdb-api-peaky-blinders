import pytest

from django.urls import reverse
from rest_framework import status

from users.fixtures import (
    api_client,
    user_data,
    user_token,
    superuser_token
)


@pytest.mark.django_db
def test_info(api_client, superuser_token, user_data):
    url = f'/api/users/info/{user_data["id"]}/'
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve user info'
    api_client.credentials(HTTP_AUTHORIZATION='Bearer wrong-token')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'Expected to fail authorization'


@pytest.mark.django_db
def test_delete_info(api_client, superuser_token, user_data):
    url = f'/api/users/info/{user_data["id"]}/'
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, 'Expected user info to be deleted'


@pytest.mark.django_db
def test_info_list(api_client, superuser_token):
    url = '/api/users/info/'
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve users info'

    api_client.credentials(HTTP_AUTHORIZATION='Bearer wrong-token')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'Expected to fail authorization for users list'


@pytest.mark.django_db
def test_change_password(api_client, user_data, user_token):
    url = f'/api/users/change_password/{user_data["id"]}/'
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    response = api_client.patch(url, {
        'username': user_data['username'],
        'old_password': user_data['password'],
        'password1': 'P@ssw0rd4322',
        'password2': 'P@ssw0rd4322'
    }, format='json')

    assert response.status_code == status.HTTP_200_OK, 'Problem with changing password'


@pytest.mark.django_db
def test_create_account(api_client, user_data):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': user_data['username'],
        'password': user_data['password']
    }, format='json')
    assert response.status_code == status.HTTP_200_OK, 'Problem with account creation'


@pytest.mark.django_db
def test_token_verify(api_client, user_token):
    url = reverse('token_verify')
    response = api_client.post(url, {
        'token': user_token['access']
    })
    assert response.status_code == status.HTTP_200_OK, 'Problem with token verification'


@pytest.mark.django_db
def test_token_refresh(api_client, user_token):
    url = reverse('token_refresh')
    response = api_client.post(url, {
        'refresh': user_token['refresh']
    })
    assert response.status_code == status.HTTP_200_OK, 'Problem with token refresh'


@pytest.mark.django_db
def test_token_logout(api_client, user_token):
    url = reverse('auth_logout')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    response = api_client.post(url, {
        'refresh': user_token['refresh']
    })
    assert response.status_code == status.HTTP_205_RESET_CONTENT, 'Problem with logging out'

    url = reverse('token_refresh')
    response = api_client.post(url, {
        'refresh': user_token['refresh']
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'User is still logged in'