from decimal import Decimal

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


def name_validator(value):
    for char in value:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError("Name can only contain letters and spaces")


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[name_validator, ])
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message='Age must be greater than or equal to 18')])

    email = models.EmailField(error_messages={'invalid': 'Enter a valid email address'})

    phone_number = models.CharField(max_length=13,
                                    validators=[validators.RegexValidator(
                                        regex=r"^\+359\d{9}$",
                                        message="Phone number must start with '+359' followed by 9 digits")])

    website_url = models.URLField(error_messages={'invalid': "Enter a valid URL"})


class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"

    author = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(5, message='Author must be at least 5 characters long')])

    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[validators.MinLengthValidator(6,
                                                  message='ISBN must be at least 6 characters long')])


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"

    director = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(8,
                                                  message='Director must be at least 8 characters long')])


class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"

    artist = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(9,
                                                  message='Artist must be at least 9 characters long')])


def calculate_shipping_cost(weight: Decimal):
    return weight * 2


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return float(self.price) * 0.08

    def calculate_shipping_cost(self, weight: Decimal):
        return float(weight) * 2.00

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        return float(self.price) * 1.20

    def calculate_tax(self):
        return float(self.price) * 0.05

    def calculate_shipping_cost(self, weight: Decimal):
        return float(weight) * 1.50

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


class RechargeEnergyMixin:
    def recharge_energy(self, amount: int):
        self.energy += amount
        self.save()
        if self.energy > 100:
            self.energy = 100
            self.save()


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()


class SpiderHero(Hero):
    class Meta:
        proxy = True

    def swing_from_buildings(self):
        if self.energy < 80:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        else:
            self.energy -= 80
            self.save()
            if self.energy == 0:
                self.energy = 1
                self.save()
            return f"{self.name} as Spider Hero swings from buildings using web shooters"


class FlashHero(Hero):
    class Meta:
        proxy = True

    def run_at_super_speed(self):
        if self.energy < 65:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        else:
            self.energy -= 65
            self.save()
            if self.energy == 0:
                self.energy = 1
                self.save()
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"
