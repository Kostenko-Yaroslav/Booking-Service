import pytest
import datetime
from django.urls import reverse
from rest_framework import status
from service.models import Booking

@pytest.mark.django_db
def test_room_list_search_filter(auth_client, room):
    url = reverse('room-list')

    response = auth_client.get(f"{url}?search={room.name}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    
    response = auth_client.get(f"{url}?search=NonExistentRoom")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 0

@pytest.mark.django_db
def test_create_booking_endpoint(auth_client, room):
    url = reverse('booking-list')
    start_date = datetime.date.today() + datetime.timedelta(days=10)
    end_date = start_date + datetime.timedelta(days=2)
    
    data = {
        "room": room.id,
        "start_date": start_date,
        "end_date": end_date
    }
    
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Booking.objects.filter(room=room).exists()

@pytest.mark.django_db
def test_booking_list_representation(auth_client, booking):
    url = reverse('booking-list')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    
    result = response.data['results'][0]

    assert result['start_date'] == booking.period.lower
    assert result['end_date'] == booking.period.upper

@pytest.mark.django_db
def test_cancel_booking_action(auth_client, booking):
    url = reverse('booking-cancel', kwargs={'pk': booking.pk})
    response = auth_client.patch(url)
    assert response.status_code == status.HTTP_200_OK
    booking.refresh_from_db()
    assert booking.cancelled is True
