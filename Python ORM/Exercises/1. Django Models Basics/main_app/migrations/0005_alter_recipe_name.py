# Generated by Django 5.0.4 on 2024-06-19 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
