import pytest
import datetime
from django.utils import timezone
from django.db.backends.postgresql.psycopg_any import DateRange
from rest_framework.test import APIClient
from users.models import CustomUser
from service.models import Room, Booking

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory(db):
    def create_user(username, password="password123"):
        user = CustomUser.objects.create_user(username=username, password=password)
        return user
    return create_user

@pytest.fixture
def user(user_factory):
    return user_factory(username="testuser")

@pytest.fixture
def other_user(user_factory):
    return user_factory(username="otheruser")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def room(db):
    return Room.objects.create(
        name="Standard Room",
        address="123 Main St",
        capacity=2,
        rating=4.5,
        price_per_night=100.00
    )

@pytest.fixture
def booking(user, room):
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=3)
    return Booking.objects.create(
        user=user,
        room=room,
        period=DateRange(start_date, end_date, bounds='[)'),
        total_price=300.00
    )
