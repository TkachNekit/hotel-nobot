from datetime import datetime

from rest_framework import filters
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from rooms.models import Room
from rooms.serializers import RoomSerializer


def filter_by_price(request, rooms_queryset):
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    if min_price:
        rooms_queryset = rooms_queryset.filter(current_price__gte=min_price)
    if max_price:
        rooms_queryset = rooms_queryset.filter(current_price__lte=max_price)
    return rooms_queryset


def filter_by_min_capacity(request, rooms_queryset):
    capacity = request.query_params.get('capacity')
    if capacity:
        rooms_queryset = rooms_queryset.filter(capacity__gte=capacity)
    return rooms_queryset


def filter_by_availability(request, rooms_queryset):
    checkin_date_str = request.query_params.get('checkin')
    checkout_date_str = request.query_params.get('checkout')
    if checkin_date_str and checkout_date_str:
        try:
            checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
        except ValueError:
            raise RestValidationError({'detail': "Invalid date format"})

        room_ids = [room.id for room in rooms_queryset if room.is_room_available_for(checkin_date, checkout_date)]

        rooms_queryset = rooms_queryset.filter(id__in=room_ids)
    return rooms_queryset


def sort_queryset(request, rooms_queryset):
    sort_by = request.query_params.get('sort_by')
    if sort_by:
        if sort_by == 'price_asc':
            rooms_queryset = rooms_queryset.order_by('current_price')
        elif sort_by == 'price_desc':
            rooms_queryset = rooms_queryset.order_by('-current_price')
        elif sort_by == 'capacity_asc':
            rooms_queryset = rooms_queryset.order_by('capacity')
        elif sort_by == 'capacity_desc':
            rooms_queryset = rooms_queryset.order_by('-capacity')
    return rooms_queryset


class RoomFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, rooms_queryset, view):
        rooms_queryset = filter_by_price(request, rooms_queryset)
        rooms_queryset = filter_by_min_capacity(request, rooms_queryset)
        rooms_queryset = filter_by_availability(request, rooms_queryset)
        rooms_queryset = sort_queryset(request, rooms_queryset)
        return rooms_queryset


class RoomModelViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [RoomFilter]

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        return super(RoomModelViewSet, self).get_permissions()
