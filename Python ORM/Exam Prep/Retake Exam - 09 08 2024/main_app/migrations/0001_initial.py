# Generated by Django 5.0.4 on 2024-08-12 14:25

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(5)])),
                ('motto', models.TextField(blank=True, null=True)),
                ('is_ruling', models.BooleanField(default=False)),
                ('castle', models.CharField(blank=True, max_length=80, null=True)),
                ('wins', models.SmallIntegerField(default=0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dragon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(5)])),
                ('power', models.DecimalField(decimal_places=1, default=1.0, max_digits=3, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)])),
                ('breath', models.CharField(choices=[('Fire', 'Fire'), ('Ice', 'Ice'), ('Lightning', 'Lightning'), ('Unknown', 'Unknown')], default='Unknown', max_length=9)),
                ('is_healthy', models.BooleanField(default=True)),
                ('birth_date', models.DateField(default=datetime.date.today)),
                ('wins', models.SmallIntegerField(default=0)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dragon_house', to='main_app.house')),
            ],
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(5)])),
                ('code', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex='^[A-Za-z#]{4}')])),
                ('reward', models.FloatField(default=100.0)),
                ('start_time', models.DateTimeField()),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('dragons', models.ManyToManyField(related_name='dragon_quests', to='main_app.dragon')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quest_house', to='main_app.house')),
            ],
        ),
    ]
