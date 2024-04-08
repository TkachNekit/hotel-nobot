from datetime import date

import pytest
from rest_framework.exceptions import ValidationError

from bookings.models import Booking
from rooms.models import Room, RoomType
from rooms.views import filter_by_availability
from users.models import User


@pytest.fixture
def rooms_queryset(db):
    # Create test rooms
    room_type = RoomType.objects.create(name='Test')
    Room.objects.create(number=101, type=room_type, current_price=100, capacity=2)
    Room.objects.create(number=102, type=room_type, current_price=150, capacity=2)
    Room.objects.create(number=103, type=room_type, current_price=200, capacity=3)
    Room.objects.create(number=104, type=room_type, current_price=250, capacity=3)
    return Room.objects.all()


@pytest.fixture
def bookings(db, rooms_queryset):
    # Create test bookings
    user = User.objects.create(username='test', first_name='test', last_name='test', email='email@mail.ru')
    Booking.objects.create(user=user, room=rooms_queryset[0], checkin_date=date(2024, 4, 10),
                           checkout_date=date(2024, 4, 15))
    Booking.objects.create(user=user, room=rooms_queryset[1], checkin_date=date(2024, 4, 16),
                           checkout_date=date(2024, 4, 20))
    return Booking.objects.all()


@pytest.mark.django_db
def test_filter_by_availability_with_valid_dates(rooms_queryset, bookings):
    # Test filtering by availability with valid dates
    request = type('', (), {'query_params': {'checkin': '2024-04-01', 'checkout': '2024-04-09'}})
    filtered_rooms = filter_by_availability(request, rooms_queryset)
    assert filtered_rooms.count() == 4  # Expecting all rooms to be available


@pytest.mark.django_db
def test_filter_by_availability_with_invalid_dates(rooms_queryset, bookings):
    # Test filtering by availability with invalid dates
    request = type('', (), {'query_params': {'checkin': 'invalid_date', 'checkout': 'invalid_date'}})
    with pytest.raises(ValidationError):
        filter_by_availability(request, rooms_queryset)


@pytest.mark.django_db
def test_filter_by_availability_with_booked_rooms(rooms_queryset, bookings):
    # Test filtering by availability with booked rooms
    request = type('', (), {'query_params': {'checkin': '2024-04-10', 'checkout': '2024-04-15'}})
    filtered_rooms = filter_by_availability(request, rooms_queryset)
    assert filtered_rooms.count() == 3  # Expecting one room to be unavailable
