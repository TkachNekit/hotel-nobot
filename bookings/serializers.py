from rest_framework import serializers

from bookings.models import Booking
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    status = serializers.ChoiceField(choices=Booking.STATUSES, source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'room', 'checkin_date', 'checkout_date', 'booking_date', 'status',)
        read_only_fields = ('booking_date',)
