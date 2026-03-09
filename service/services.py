from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.db.backends.postgresql.psycopg_any import DateRange

from service.models import Booking
from service.tasks import send_email

def cancel_booking(booking, user):
    if booking.user != user:
        raise ValidationError("You cannot cancel someone else's reservation.")
    if booking.cancelled:
        raise ValidationError("The reservation has already been cancelled.")

    booking.cancelled = True
    booking.save(update_fields=['cancelled']) # обновляем
    return booking

def create_booking(start_date, end_date, user, room):
    count_date = (end_date - start_date).days
    total_price = count_date * room.price_per_night
    period = DateRange(start_date, end_date, bounds='[)')

    try:
        booking = Booking.objects.create(
            user=user,
            room=room,
            total_price=total_price,
            period=period,
        )
    except IntegrityError as e:
        error_message = str(e).lower()
        if "exclude_overlapping_reservations" in error_message:
            raise ValidationError({"room": "This room is already booked for the selected dates."})

    send_email.delay(booking.id)

    return booking