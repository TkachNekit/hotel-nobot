# Generated by Django 4.2.11 on 2024-04-08 13:02

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RoomType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.PositiveSmallIntegerField(unique=True)),
                (
                    "current_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "capacity",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rooms.roomtype"
                    ),
                ),
            ],
        ),
    ]
