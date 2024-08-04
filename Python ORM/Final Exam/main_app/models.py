from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator

from main_app.validators import digits_val

from main_app.custom_manager import AstronautsManager


class Astronaut(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    phone_number = models.CharField(max_length=15, unique=True, validators=[digits_val, ])
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    objects = AstronautsManager()


class Spacecraft(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.SmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    STATUS_CHOICES = (('Planned', 'Planned'),
                      ('Ongoing', 'Ongoing'),
                      ('Completed', 'Completed'))

    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9, default='Planned', choices=STATUS_CHOICES)
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='mission_spacecraft')
    astronauts = models.ManyToManyField(Astronaut, related_name='mission_astronauts')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='mission_commander')
