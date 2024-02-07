# Generated by Django 4.2.6 on 2023-11-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0004_item_is_sold'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rentitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rentitem_Date_of_Booking', models.DateField(blank=True, null=True)),
                ('Rentitem_Date_of_Return', models.DateField(blank=True, null=True)),
                ('Total_days', models.IntegerField()),
                ('Advance_amount', models.IntegerField(blank=True, null=True)),
                ('Rentitem_Total_amount', models.IntegerField(blank=True, null=True)),
                ('isAvailable', models.BooleanField(default=True)),
                ('customer_email', models.CharField(max_length=100)),
                ('request_responded_by', models.CharField(blank=True, max_length=100, null=True)),
                ('request_status', models.CharField(default='Pending', max_length=30)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explore.item')),
            ],
        ),
        migrations.DeleteModel(
            name='Rentinstrument',
        ),
    ]