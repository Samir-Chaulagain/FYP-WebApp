# Generated by Django 5.0.2 on 2024-02-19 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0017_booking_invoice_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_available',
            new_name='is_unavailable',
        ),
    ]