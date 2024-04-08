from django.urls import include, path, re_path
from rest_framework import routers

from bookings.views import BookingModelViewSet
from rooms.views import RoomModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'rooms', RoomModelViewSet)
router.register(r'bookings', BookingModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
