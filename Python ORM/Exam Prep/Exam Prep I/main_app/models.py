from django.db import models

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from main_app.custom_manager import DirectorManager


# Create your models here.
class Director(models.Model):
    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default="Unknown")
    years_of_experience = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0)
    objects = DirectorManager()

    def __str__(self):
        return self.full_name


class Actor(models.Model):
    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default="Unknown")
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Movie(models.Model):
    GENRE_CHOICES = (('Action', 'Action'),
                     ('Comedy', 'Comedy'),
                     ('Drama', 'Drama'),
                     ('Other', 'Other'))
    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=6, default='Other', choices=GENRE_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0.0)
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movie_director')
    starring_actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='movie_star')
    actors = models.ManyToManyField(Actor, related_name='movie_actors')

    def __str__(self):
        return self.title
