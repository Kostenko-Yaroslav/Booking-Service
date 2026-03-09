from django.db.backends.postgresql.psycopg_any import DateRange
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from service.models import Booking, Room


class RoomFilter(filters.FilterSet):
    check_in = filters.DateFilter(method='filter_date', help_text='Start date.')
    check_out = filters.DateFilter(method='filter_date', help_text='End date.')
    max_price = filters.NumberFilter(field_name='price_per_night', lookup_expr='lte', help_text='Maximum price.')
    min_price = filters.NumberFilter(field_name='price_per_night', lookup_expr='gte', help_text='Minimum price.')
    specialties = filters.NumberFilter(field_name='specialties__id', help_text='Specialty ID.')

    order_by = filters.OrderingFilter(
        fields=(
        ('price_per_night', 'price'),
        )
    )

    class Meta:
        model = Room
        fields = ['capacity']

    def filter_date(self, queryset, name, value):
        start_date = self.data.get('check_in')
        end_date = self.data.get('check_out')

        if not start_date or not end_date:
            return queryset

        if start_date >= end_date:
            raise ValidationError({'check_in': 'Invalid dates.'})

        data_period = DateRange(start_date, end_date, bounds='[)')
        booked_rooms = Booking.objects.filter(
            period__overlap=data_period,
            cancelled=False,
        ).values_list('room_id', flat=True)

        return queryset.exclude(id__in=booked_rooms)

class BookingFilter(filters.FilterSet):
    check_in = filters.DateFilter(method='filter_date', help_text='Start date.')
    check_out = filters.DateFilter(method='filter_date', help_text='End date.')

    class Meta:
        model = Booking
        fields = ['cancelled']

    def filter_date(self, queryset, name, value):
        start_date = self.data.get('check_in')
        end_date = self.data.get('check_out')

        if not start_date or not end_date:
            return queryset

        if start_date >= end_date:
            raise ValidationError({'check_in': 'Invalid dates.'})

        data_period = DateRange(start_date, end_date, bounds='[)')
        booked_rooms = Booking.objects.filter(
            period__overlap=data_period,
            cancelled=False,
        ).values_list('room_id', flat=True)

        return queryset.filter(room_id__in=booked_rooms)




