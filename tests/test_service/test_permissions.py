import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_anonymous_permissions(api_client, room, booking):
    response = api_client.get(reverse('room-list'))
    assert response.status_code == status.HTTP_200_OK
    
    response = api_client.post(reverse('booking-list'), {"room": room.id})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    response = api_client.patch(reverse('booking-cancel', kwargs={'pk': booking.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_user_cannot_cancel_others_booking(api_client, other_user, booking):
    api_client.force_authenticate(user=other_user)
    
    url = reverse('booking-cancel', kwargs={'pk': booking.pk})
    response = api_client.patch(url)

    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
