from django.core.mail import EmailMessage
from celery import shared_task
from django.conf import settings
from service.models import Booking
from service.pdf_generator import BookingInvoice


@shared_task
def send_email(booking_id):
    try:
        booking = Booking.objects.select_related('room', 'user').get(id=booking_id)
    except Booking.DoesNotExist:
        return

    user = booking.user

    def generate_invoice():
        data = {
            "booking_id": booking.id,
            "username": user.username,
            "room_name": booking.room.name,
            "room_address": booking.room.address,
            "room_capacity": booking.room.capacity,
            "date_period": str(booking.period),
            "total_price": booking.total_price,
        }

        pdf = BookingInvoice()
        pdf.create_invoice(data)

        return bytes(pdf.output())

    subject = "Invoice"
    pdf_content = generate_invoice()

    email = EmailMessage(
        subject=subject,
        body="Invoice",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach(
        filename=f"invoice_{booking.id}.pdf",
        content=pdf_content,
        mimetype="application/pdf",
    )
    email.send()


