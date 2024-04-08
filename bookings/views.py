from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookings.models import Booking
from rooms.models import Room
from bookings.serializers import BookingSerializer


class BookingModelViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return super(BookingModelViewSet, self).get_queryset()
        else:
            queryset = super(BookingModelViewSet, self).get_queryset()
            return queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'destroy',):
            self.permission_classes = (IsAdminUser,)
        return super(BookingModelViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            room_number = request.data['room_number']

            checkin_date = datetime.strptime(request.data['checkin_date'], '%d-%m-%Y').date()
            checkout_date = datetime.strptime(request.data['checkout_date'], '%d-%m-%Y').date()

            if not Room.objects.filter(number=room_number).exists():
                return Response({'room_number': 'There is no room with this number'},
                                status=status.HTTP_400_BAD_REQUEST)

            room = Room.objects.get(number=room_number)
            difference = checkout_date - checkin_date

            booking = Booking.objects.create(user=self.request.user, room=room, checkin_date=checkin_date,
                                             checkout_date=checkout_date, price=room.current_price * difference.days)

            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({'dates': "Date does not match the format %d-%m-%Y"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'dates': e.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = Booking.CANCELED
        booking.save(update_fields=['status'])
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
