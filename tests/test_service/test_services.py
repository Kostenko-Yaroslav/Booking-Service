import pytest
import datetime
from unittest import mock
from rest_framework.exceptions import ValidationError
from service.services import create_booking, cancel_booking
from service.models import Booking

@pytest.mark.django_db
def test_create_booking_logic(room, user):
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=2)
    
    with mock.patch('service.tasks.send_email.delay') as mock_send_email:
        booking = create_booking(start_date, end_date, user, room)
        
        assert booking.total_price == room.price_per_night * 2
        assert booking.user == user
        assert booking.room == room
        mock_send_email.assert_called_once_with(booking.id)

@pytest.mark.django_db
def test_create_booking_overlapping_raises_error(room, user):
    start1 = datetime.date.today()
    end1 = start1 + datetime.timedelta(days=5)
    create_booking(start1, end1, user, room)
    
    with pytest.raises(ValidationError) as exc:
        create_booking(start1, end1, user, room)
    assert "already booked" in str(exc.value)

@pytest.mark.django_db
def test_cancel_booking_success(booking, user):
    cancelled_booking = cancel_booking(booking, user)
    assert cancelled_booking.cancelled is True
    booking.refresh_from_db()
    assert booking.cancelled is True

@pytest.mark.django_db
def test_cancel_booking_already_cancelled(booking, user):
    cancel_booking(booking, user)
    with pytest.raises(ValidationError) as exc:
        cancel_booking(booking, user)
    assert "already been cancelled" in str(exc.value)

@pytest.mark.django_db
def test_cancel_other_user_booking(booking, other_user):
    with pytest.raises(ValidationError) as exc:
        cancel_booking(booking, other_user)
    assert "someone else's" in str(exc.value)
