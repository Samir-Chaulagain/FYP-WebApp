# Generated by Django 4.2.7 on 2024-01-26 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_booking_booked_at_saved_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='status',
        ),
        migrations.AddField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]