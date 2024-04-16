from datetime import datetime

import django_filters
from rest_framework.exceptions import ValidationError

from rooms.models import Room


class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'current_price': ['lte', 'gte', 'lt', 'gt'],
            'capacity': ['lte', 'gte', 'lt', 'gt'],
        }

    @classmethod
    def filter_by_availability(cls, request, rooms_queryset):
        checkin_date_str = request.query_params.get('checkin')
        checkout_date_str = request.query_params.get('checkout')
        if checkin_date_str and checkout_date_str:
            try:
                checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date()
                checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError({'detail': "Invalid date format"})

            room_ids = [room.id for room in rooms_queryset if room.is_room_available_for(checkin_date, checkout_date)]

            rooms_queryset = rooms_queryset.filter(id__in=room_ids)
        return rooms_queryset

    @classmethod
    def sort_queryset(cls, request, rooms_queryset):
        sort_by = request.query_params.get('sort_by')
        if sort_by:
            if sort_by == 'price':
                rooms_queryset = rooms_queryset.order_by('current_price')
            elif sort_by == '-price':
                rooms_queryset = rooms_queryset.order_by('-current_price')
            elif sort_by == 'capacity':
                rooms_queryset = rooms_queryset.order_by('capacity')
            elif sort_by == '-capacity':
                rooms_queryset = rooms_queryset.order_by('-capacity')
        return rooms_queryset
