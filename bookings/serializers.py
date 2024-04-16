from django.core.exceptions import ValidationError as DjangoVE
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bookings.models import Booking
from rooms.models import Room
from users.models import User


class BookingSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(slug_field='number', queryset=Room.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    status = serializers.ChoiceField(choices=Booking.STATUSES, source='get_status_display', )

    class Meta:
        model = Booking
        fields = ('id', 'user', 'room', 'checkin_date', 'checkout_date', 'booking_date', 'status', 'price')
        read_only_fields = ('booking_date',)

    def create(self, validated_data):
        try:
            booking = Booking(
                user=validated_data['user'], room=validated_data['room'],
                checkin_date=validated_data['checkin_date'], checkout_date=validated_data['checkout_date'],
                price=validated_data['price'], status=validated_data['get_status_display']
            )
            booking.full_clean()
            booking.save()
            return booking
        except DjangoVE as e:
            raise ValidationError({'message': e.message_dict['__all__'][0]})

    def update(self, instance, validated_data):
        try:
            instance.room = validated_data.get('room', instance.room)
            instance.user = validated_data.get('user', instance.user)
            instance.checkin_date = validated_data.get('checkin_date', instance.checkin_date)
            instance.checkout_date = validated_data.get('checkout_date', instance.checkout_date)
            instance.status = validated_data.get('get_status_display', instance.status)
            instance.price = validated_data.get('price', instance.price)
            if 'checkin_date' in validated_data or 'checkout_date' in validated_data or 'room' in validated_data:
                instance.full_clean()
            instance.save()
            return instance
        except DjangoVE as e:
            raise ValidationError({'message': e.message_dict['__all__'][0]})
