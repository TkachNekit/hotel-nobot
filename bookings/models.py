from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from rooms.models import Room
from users.models import User


class Booking(models.Model):
    BOOKED = 0
    CANCELED = 1
    EXPIRED = 2

    STATUSES = (
        (BOOKED, 'Booked'),
        (CANCELED, 'Canceled'),
    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, null=False, blank=False)
    checkin_date = models.DateField(null=False, blank=False)
    checkout_date = models.DateField(null=False, blank=False)
    booking_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    status = models.SmallIntegerField(default=BOOKED, choices=STATUSES)
    price = models.DecimalField(decimal_places=2, max_digits=9, validators=[MinValueValidator(Decimal('0.01'))],
                                null=False, blank=False)

    def __str__(self):
        return f"Booking on room №{self.room.number} on dates: {self.checkin_date} - {self.checkout_date}"

    def save(self, *args, **kwargs):
        # Check if only the status field is being updated
        if 'update_fields' in kwargs:
            if 'status' in kwargs['update_fields'] and len(kwargs['update_fields']) == 1:
                # Only updating the status, no need to perform room availability check
                super().save(*args, **kwargs)
        else:
            if not Room.objects.filter(number=self.room.number).exists():
                raise ValidationError("Room with given room number doesn't exist.")

            # Validate dates
            difference = self.checkout_date - self.checkin_date
            if difference.days < 1:
                raise ValidationError("Checkout date can't be earlier than 1 day after check-in.")

            # Check room availability
            if not self.room.is_room_available_for(self.checkin_date, self.checkout_date):
                raise ValidationError("Room unavailable for these dates.")

            self.price = self.room.current_price * difference.days

            super().save(*args, **kwargs)
