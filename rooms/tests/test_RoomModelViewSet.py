import pytest
from django.test import RequestFactory
from rest_framework.test import force_authenticate

from rooms.models import Room, RoomType
from rooms.views import RoomModelViewSet
from users.models import User


@pytest.fixture
def room_factory(db):
    def create_room(**kwargs):
        return Room.objects.create(**kwargs)

    return create_room


@pytest.fixture
def user():
    return User.objects.create(username='testuser', first_name="test", last_name="test", password='password')


@pytest.fixture
def super_user():
    return User.objects.create_superuser(username='superuser', first_name="test", last_name="test", password='password')


@pytest.fixture
def api_client():
    return RequestFactory()


@pytest.fixture
def view():
    return RoomModelViewSet.as_view({'get': 'list'})


@pytest.mark.django_db
def test_list_rooms(api_client, view, user, room_factory):
    # Create some rooms
    room_type = RoomType.objects.create(name='Test')
    room_factory(number=101, current_price=100, capacity=2, type=room_type)
    room_factory(number=102, current_price=150, capacity=3, type=room_type)
    room_factory(number=103, current_price=200, capacity=4, type=room_type)

    # Authenticate the request
    request = api_client.get('/api/rooms/')
    force_authenticate(request, user=user)

    # Call the view function
    response = view(request)

    # Check status code
    assert response.status_code == 200

    # Check response data
    assert len(response.data) == 3
    assert response.data[0]['number'] == 101
    assert response.data[1]['number'] == 102
    assert response.data[2]['number'] == 103


@pytest.mark.django_db
def test_create_room_as_regular_user(api_client, view, user):
    # Authenticate the request
    request = api_client.post('/api/rooms/', {'number': 104, 'type': 1, 'current_price': 120, 'capacity': 2})
    force_authenticate(request, user=user)

    # Call the view function
    response = view(request)

    # Check status code
    assert response.status_code == 405


@pytest.mark.django_db
def test_update_room_as_regular_user(api_client, view, user, room_factory):
    # Create a room
    room_type = RoomType.objects.create(name='Test')
    room = room_factory(number=105, type=room_type, current_price=100, capacity=2)

    # Authenticate the request
    request = api_client.patch(f'/api/rooms/{room.id}/', {'current_price': 150})
    force_authenticate(request, user=user)

    # Call the view function
    response = view(request, pk=room.id)

    # Check status code
    assert response.status_code == 405


@pytest.mark.django_db
def test_delete_room_as_regular_user(api_client, view, user, room_factory):
    # Create a room
    room_type = RoomType.objects.create(name='Test')
    room = room_factory(number=106, type=room_type, current_price=100, capacity=2)

    # Authenticate the request
    request = api_client.delete(f'/api/rooms/{room.id}/')
    force_authenticate(request, user=user)

    # Call the view function
    response = view(request, pk=room.id)

    # Check status code
    assert response.status_code == 405
