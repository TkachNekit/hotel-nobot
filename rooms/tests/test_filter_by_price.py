import pytest

from rooms.models import Room, RoomType
from rooms.views import filter_by_price


@pytest.fixture
def rooms_queryset(db):
    # Create test rooms with different prices
    room_type = RoomType.objects.create(name='Test')
    Room.objects.create(number=99, type=room_type, capacity=2, current_price=50)
    Room.objects.create(number=98, type=room_type, capacity=2, current_price=100)
    Room.objects.create(number=97, type=room_type, capacity=2, current_price=150)
    Room.objects.create(number=96, type=room_type, capacity=2, current_price=200)
    return Room.objects.all()


@pytest.mark.django_db
def test_filter_by_price_min_price(rooms_queryset):
    # Test filtering by minimum price
    request = type('', (), {'query_params': {'min_price': 100}})
    filtered_rooms = filter_by_price(request, rooms_queryset)
    assert filtered_rooms.count() == 3  # Expecting 3 rooms with prices >= 100


@pytest.mark.django_db
def test_filter_by_price_max_price(rooms_queryset):
    # Test filtering by maximum price
    request = type('', (), {'query_params': {'max_price': 150}})
    filtered_rooms = filter_by_price(request, rooms_queryset)
    assert filtered_rooms.count() == 3  # Expecting 3 rooms with prices <= 150


@pytest.mark.django_db
def test_filter_by_price_min_and_max_price(rooms_queryset):
    # Test filtering by both minimum and maximum price
    request = type('', (), {'query_params': {'min_price': 100, 'max_price': 200}})
    filtered_rooms = filter_by_price(request, rooms_queryset)
    assert filtered_rooms.count() == 3  # Expecting 2 rooms with prices between 100 and 200


@pytest.mark.django_db
def test_filter_by_price_no_price_filter(rooms_queryset):
    # Test when no price filter is provided
    request = type('', (), {'query_params': {}})
    filtered_rooms = filter_by_price(request, rooms_queryset)
    assert filtered_rooms.count() == 4  # Expecting all rooms to be returned
