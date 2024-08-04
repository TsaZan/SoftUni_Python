# Generated by Django 5.0.4 on 2024-07-24 21:19

import main_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='restaurant',
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.TextField(validators=[main_app.validators.category_validator]),
        ),
    ]
