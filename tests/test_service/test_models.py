import pytest
import datetime
from django.db import IntegrityError
from django.db.backends.postgresql.psycopg_any import DateRange
from service.models import Room, Booking

@pytest.mark.django_db
def test_room_capacity_constraint():
    with pytest.raises(IntegrityError):
        Room.objects.create(
            name="Invalid Room",
            address="Addr",
            capacity=0,
            rating=0,
            price_per_night=10
        )

@pytest.mark.django_db
def test_overlapping_bookings_constraint(room, user):
    start1 = datetime.date.today()
    end1 = start1 + datetime.timedelta(days=5)
    
    Booking.objects.create(
        user=user,
        room=room,
        period=DateRange(start1, end1, bounds='[)'),
        total_price=500
    )
    
    start2 = start1 + datetime.timedelta(days=2)
    end2 = start2 + datetime.timedelta(days=5)
    
    with pytest.raises(IntegrityError):
        Booking.objects.create(
            user=user,
            room=room,
            period=DateRange(start2, end2, bounds='[)'),
            total_price=500
        )

@pytest.mark.django_db
def test_overlapping_allowed_if_cancelled(room, user):
    start1 = datetime.date.today()
    end1 = start1 + datetime.timedelta(days=5)
    
    Booking.objects.create(
        user=user,
        room=room,
        period=DateRange(start1, end1, bounds='[)'),
        total_price=500,
        cancelled=True
    )
    
    Booking.objects.create(
        user=user,
        room=room,
        period=DateRange(start1, end1, bounds='[)'),
        total_price=500
    )

@pytest.mark.django_db
def test_touching_dates_allowed(room, user):
    start1 = datetime.date.today()
    end1 = start1 + datetime.timedelta(days=5)
    
    Booking.objects.create(
        user=user,
        room=room,
        period=DateRange(start1, end1, bounds='[)'),
        total_price=500
    )
    
    start2 = end1
    end2 = start2 + datetime.timedelta(days=5)
    
    Booking.objects.create(
        user=user,
        room=room,
        period=DateRange(start2, end2, bounds='[)'),
        total_price=500
    )
