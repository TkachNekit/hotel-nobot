from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from rooms.models import Room
from users.models import User


class Booking(models.Model):
    BOOKED = 0
    CANCELED = 1

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

    def clean(self):
        if not self.room.is_room_available_for(checkin_date=self.checkin_date, checkout_date=self.checkout_date):
            raise ValidationError("This room is already booked on this dates")
        if not self.checkin_date < self.checkout_date:
            raise ValidationError("Checkout day should be at least 1 day after checkin")
