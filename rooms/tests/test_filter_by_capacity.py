import pytest

from rooms.models import Room, RoomType
from rooms.views import filter_by_min_capacity


@pytest.fixture
def rooms_queryset(db):
    # Create test rooms with different capacities
    room_type = RoomType.objects.create(name='Test')
    Room.objects.create(number=99, type=room_type, capacity=2, current_price=50)
    Room.objects.create(number=98, type=room_type, capacity=3, current_price=100)
    Room.objects.create(number=97, type=room_type, capacity=4, current_price=150)
    Room.objects.create(number=96, type=room_type, capacity=5, current_price=200)
    return Room.objects.all()


@pytest.mark.django_db
def test_filter_by_capacity_with_capacity_filter(rooms_queryset):
    # Test filtering by capacity
    request = type('', (), {'query_params': {'capacity': 3}})
    filtered_rooms = filter_by_min_capacity(request, rooms_queryset)
    assert filtered_rooms.count() == 3  # Expecting 1 room with capacity >= 3


@pytest.mark.django_db
def test_filter_by_capacity_without_capacity_filter(rooms_queryset):
    # Test when no capacity filter is provided
    request = type('', (), {'query_params': {}})
    filtered_rooms = filter_by_min_capacity(request, rooms_queryset)
    assert filtered_rooms.count() == 4  # Expecting all rooms to be returned
