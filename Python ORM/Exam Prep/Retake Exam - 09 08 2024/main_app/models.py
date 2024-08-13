from datetime import date

from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from custom_manager import HouseManager


# Create your models here.


class House(models.Model):
    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)], unique=True)
    motto = models.TextField(blank=True, null=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(max_length=80, blank=True, null=True)
    wins = models.PositiveSmallIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)

    objects = HouseManager()
class Dragon(models.Model):
    BREATH_CHOICES = (("Fire", "Fire"),
                      ("Ice", "Ice"),
                      ("Lightning", "Lightning"),
                      ("Unknown", "Unknown"))

    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)],unique=True)
    power = models.DecimalField(max_digits=3, decimal_places=1,
                                validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], default=1.0)
    breath = models.CharField(max_length=9, default='Unknown', choices=BREATH_CHOICES)
    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField(default=date.today)
    wins = models.SmallIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='dragon_house')


class Quest(models.Model):
    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)], unique=True)
    code = models.CharField(max_length=4, validators=[RegexValidator(regex=r'^[A-Za-z#]{4}')])
    reward = models.FloatField(default=100.0)
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)
    dragons = models.ManyToManyField(Dragon, related_name='dragon_quests')
    host = models.ForeignKey(House, on_delete=models.CASCADE, related_name='quest_house')
