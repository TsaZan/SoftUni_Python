# Generated by Django 5.0.4 on 2024-07-20 17:48

import main_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogame',
            name='release_year',
            field=models.PositiveIntegerField(validators=[main_app.validators.ReleaseYearValidator]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='title',
            field=models.CharField(max_length=100, validators=[main_app.validators.MovieRatingValidator]),
        ),
    ]
