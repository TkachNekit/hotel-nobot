from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookings.models import Booking
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

    def partial_update(self, request, *args, **kwargs):
        try:
            if not self.request.user.is_staff:  # ограничиваем для обычного пользователя функционал
                if len(request.data) > 1 or 'status' not in request.data:
                    return Response({'arguments': 'Regular user can ONLY PATCH status in booking'},
                                    status=status.HTTP_400_BAD_REQUEST)
                if 'status' in request.data and request.data['status'] != str(Booking.CANCELED):
                    return Response({'status': 'Regular user can ONLY PATCH booking status to cancel it'},
                                    status=status.HTTP_400_BAD_REQUEST)

            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except ValueError as e:
            return Response({'dates': str(e)}, status=status.HTTP_400_BAD_REQUEST)
