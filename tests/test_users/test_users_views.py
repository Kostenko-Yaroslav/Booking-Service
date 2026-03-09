import pytest
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser

@pytest.mark.django_db
def test_user_registration_success(api_client):
    url = reverse('register')
    data = {
        "username": "newuser",
        "password": "password123",
        "email": "new@example.com"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    
    user = CustomUser.objects.get(username="newuser")
    assert user.password != "password123"
    assert user.check_password("password123")

@pytest.mark.django_db
def test_duplicate_username_returns_400(api_client, user):
    url = reverse('register')
    data = {
        "username": user.username,
        "password": "password123",
        "email": "new@example.com"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_incomplete_data_returns_400(api_client):
    url = reverse('register')
    data = {
        "username": "incomplete_user",
        "email": "inc@example.com"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
