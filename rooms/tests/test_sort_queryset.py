import pytest

from rooms.models import Room, RoomType
from rooms.views import sort_queryset


@pytest.fixture
def rooms_queryset(db):
    # Create test rooms
    room_type = RoomType.objects.create(name='Test')
    Room.objects.create(number=101, type=room_type, current_price=100, capacity=2)
    Room.objects.create(number=102, type=room_type, current_price=150, capacity=2)
    Room.objects.create(number=103, type=room_type, current_price=200, capacity=3)
    Room.objects.create(number=104, type=room_type, current_price=250, capacity=3)
    return Room.objects.all()


@pytest.mark.django_db
def test_sort_queryset_price_asc(rooms_queryset):
    # Test sorting by price in ascending order
    request = type('', (), {'query_params': {'sort_by': 'price_asc'}})
    sorted_rooms = sort_queryset(request, rooms_queryset)
    assert list(sorted_rooms) == [room for room in rooms_queryset.order_by('current_price')]


@pytest.mark.django_db
def test_sort_queryset_price_desc(rooms_queryset):
    # Test sorting by price in descending order
    request = type('', (), {'query_params': {'sort_by': 'price_desc'}})
    sorted_rooms = sort_queryset(request, rooms_queryset)
    assert list(sorted_rooms) == [room for room in rooms_queryset.order_by('-current_price')]


@pytest.mark.django_db
def test_sort_queryset_capacity_asc(rooms_queryset):
    # Test sorting by capacity in ascending order
    request = type('', (), {'query_params': {'sort_by': 'capacity_asc'}})
    sorted_rooms = sort_queryset(request, rooms_queryset)
    assert list(sorted_rooms) == [room for room in rooms_queryset.order_by('capacity')]


@pytest.mark.django_db
def test_sort_queryset_capacity_desc(rooms_queryset):
    # Test sorting by capacity in descending order
    request = type('', (), {'query_params': {'sort_by': 'capacity_desc'}})
    sorted_rooms = sort_queryset(request, rooms_queryset)
    assert list(sorted_rooms) == [room for room in rooms_queryset.order_by('-capacity')]
