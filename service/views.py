from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from service.filters import RoomFilter, BookingFilter
from service.models import Room, Booking
from service.permissions import RoomPermission, BookingPermission
from service.serializers import RoomSerializer, BookingSerializer

from . import services

@extend_schema_view(
    list=extend_schema(auth=[]),
    retrieve=extend_schema(auth=[])
)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.prefetch_related('specialties').order_by('id')
    serializer_class = RoomSerializer
    permission_classes = (RoomPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RoomFilter
    search_fields = ['name', 'address']
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('id')
    serializer_class = BookingSerializer
    permission_classes = (BookingPermission, )

    http_method_names = ['get', 'post', 'patch']

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BookingFilter
    search_fields = ['room__name', 'room__address']

    def get_queryset(self):
        qs = Booking.objects.select_related('room', 'user').order_by('id')
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        booking = services.create_booking(
            user=self.request.user,
            room=serializer.validated_data['room'],
            start_date=serializer.validated_data['start_date'],
            end_date=serializer.validated_data['end_date'],
        )
        serializer.instance = booking

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        services.cancel_booking(booking, user=request.user)
        return Response('Cancelled', status=status.HTTP_200_OK)