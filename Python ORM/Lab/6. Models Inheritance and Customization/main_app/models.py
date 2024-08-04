from django.db import models
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from math import floor


# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) <
                (self.birth_date.month, self.birth_date.day))


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)


class ZooKeeper(Employee):
    class SPECIALTY_CHOICES(models.TextChoices):
        Mammals = 'Mammals'
        Birds = 'Birds'
        Reptiles = 'Reptiles'
        Others = 'Others'

    specialty = models.CharField(max_length=10, choices=SPECIALTY_CHOICES)
    managed_animals = models.ManyToManyField(to=Animal)

    def clean(self):
        super().clean()
        if self.specialty not in self.SPECIALTY_CHOICES:
            raise ValidationError('Specialty must be a valid choice.')


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, 'Available'),
                             (False, 'Not Available'))

        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

    def is_available(self):
        return self.availability


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    AT_RISK = ["Cross River Gorilla", "Orangutan", "Green Turtle"]

    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        if self.species in self.AT_RISK:
            return f"{self.species} is at risk!"
        else:
            return f"{self.species} is not at risk."
