# Generated by Django 5.0.4 on 2024-06-20 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_exercise_equipment_alter_exercise_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='calories_burned',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
