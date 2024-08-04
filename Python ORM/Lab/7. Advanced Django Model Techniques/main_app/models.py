from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.validators import category_validator


# Create your models here.
class ReviewMixin(models.Model):
    class Meta:
        abstract = True

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), ])
    review_content = models.TextField()

class Restaurant(models.Model):
    name = models.CharField(max_length=100,
                            validators=
                            [MinLengthValidator(2, message='Name must be at least 2 characters long.'),
                             MaxLengthValidator(100, message='Name cannot exceed 100 characters.')])

    location = models.CharField(max_length=200,
                                validators=[
                                    MinLengthValidator(2, message='Location must be at least 2 characters long.'),
                                    MaxLengthValidator(200, message='Location cannot exceed 200 characters.')])
    description = models.TextField(blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[MinValueValidator(0.00, message="Rating must be at least 0.00."),
                                             MaxValueValidator(5.00, message="Rating cannot exceed 5.00.")])


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[category_validator, ])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class RestaurantReview(ReviewMixin):
    class Meta:
        abstract = True
        verbose_name = "Restaurant Review"
        verbose_name_plural = "Restaurant Reviews"
        unique_together = ['reviewer_name', 'restaurant']
        ordering = ['-rating']

    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(to='Restaurant', on_delete=models.CASCADE)


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    class Meta:
        ordering = ['-rating']
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'
        unique_together = ['reviewer_name', 'restaurant']

    food_critic_cuisine_area = models.CharField(max_length=100)


class MenuReview(ReviewMixin):
    class Meta:
        ordering = ['-rating']
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ['reviewer_name', 'menu']
        indexes = [models.Index(fields=['menu'], name="main_app_menu_review_menu_id")]

    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(to='Menu', on_delete=models.CASCADE)
