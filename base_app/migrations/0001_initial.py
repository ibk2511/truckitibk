# Generated by Django 3.0.5 on 2020-04-27 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('aadhar_id', models.CharField(max_length=16)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('aadhar_id', models.CharField(max_length=16)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=20)),
                ('make', models.CharField(max_length=20)),
                ('capacity', models.FloatField(default=0)),
                ('wheels', models.PositiveSmallIntegerField(default=0)),
                ('is_rented', models.BooleanField(default=False)),
                ('rate_per_day', models.IntegerField()),
                ('is_requested', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='base_app.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='TruckRent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('pickup_time', models.DateTimeField(default=None)),
                ('drop_time', models.DateTimeField(default=None)),
                ('is_dropped', models.BooleanField(default=False)),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.Truck')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.Client')),
            ],
        ),
    ]
