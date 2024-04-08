from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=128, blank=False, null=False)
    last_name = models.CharField(max_length=128, blank=False, null=False)
    username = models.CharField(max_length=128, blank=False, null=False, unique=True,
                                validators=[UnicodeUsernameValidator()])
    email = models.EmailField(blank=False, null=False, unique=True)

    REQUIRED_FIELDS = ('first_name', 'last_name', 'email',)
