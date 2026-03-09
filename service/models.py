from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators, DateRangeField
from django.db import models
from django.db.models import Q, CheckConstraint

from users.models import CustomUser

class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, db_index=True)
    capacity = models.IntegerField(db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    specialties = models.ManyToManyField(Specialty)

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(capacity__gt=0),
                name='capacity_greater_than',
            )
        ]


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    period = DateRangeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    cancelled = models.BooleanField(default=False)

    class Meta:
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations',
                expressions=[
                    ('period', RangeOperators.OVERLAPS),
                    ('room', RangeOperators.EQUAL),
                ],
                condition=Q(cancelled=False),
            ),
        ]