import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from users.serializers import UserSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data(db):
    user_info = {
        'username': 'user',
        'email': 'user@email.com',
        'password': 'P@ssw0rd4321'
    }
    user = User.objects.create_user(**user_info)
    user_data = UserSerializer(user).data
    user_data['password'] = user_info['password']
    return user_data


@pytest.fixture
def user_token(api_client, user_data):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': user_data['username'],
        'password': user_data['password']
    }, format='json')
    return response.data


@pytest.fixture
def superuser_token(api_client, admin_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'admin',
        'password': 'password'
    }, format='json')
    return response.data


@pytest.mark.django_db
def test_info(api_client, superuser_token, user_data):
    url = f'/api/users/info/{user_data["id"]}/'
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    api_client.credentials(HTTP_AUTHORIZATION='Bearer wrong-token')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_info(api_client, superuser_token, user_data):
    url = f'/api/users/info/{user_data["id"]}/'
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_info_list(api_client, superuser_token):
    url = '/api/users/info/'
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    api_client.credentials(HTTP_AUTHORIZATION='Bearer wrong-token')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_change_password(api_client, user_data, user_token):
    url = f'/api/users/change_password/{user_data["id"]}/'
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    response_change = api_client.patch(url, {
        'username': user_data['username'],
        'old_password': user_data['password'],
        'password1': 'P@ssw0rd4322',
        'password2': 'P@ssw0rd4322'
    }, format='json')

    assert response_change.status_code == status.HTTP_200_OK, 'Problem with changing password'


@pytest.mark.django_db
def test_create_account(api_client, user_data):
    url = reverse('token_obtain_pair')
    resp = api_client.post(url, {
        'username': user_data['username'],
        'password': user_data['password']
    }, format='json')
    assert resp.status_code == status.HTTP_200_OK, 'Problem with account creation'


@pytest.mark.django_db
def test_token_verify(api_client, user_token):
    url = reverse('token_verify')
    response = api_client.post(url, {
        'token': user_token['access']
    })
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_token_refresh(api_client, user_token):
    url = reverse('token_refresh')
    response = api_client.post(url, {
        'refresh': user_token['refresh']
    })
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_token_logout(api_client, user_token):
    url = reverse('auth_logout')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    response = api_client.post(url, {
        'refresh': user_token['refresh']
    })
    assert response.status_code == status.HTTP_205_RESET_CONTENT

    url = reverse('token_refresh')
    response = api_client.post(url, {
        'refresh': user_token['refresh']
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
