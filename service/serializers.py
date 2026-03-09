from service.models import Room, Booking
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(min_value=1)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, default=0)
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'total_price', 'start_date', 'end_date', 'cancelled']
        read_only_fields = ['id', 'user', 'total_price', 'cancelled']

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError('Start date must be before end date')
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['start_date'] = instance.period.lower
        ret['end_date'] = instance.period.upper
        return ret