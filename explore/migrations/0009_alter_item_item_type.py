# Generated by Django 4.2.6 on 2023-11-20 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0008_item_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('1', 'Solo'), ('2', 'Package'), ('3', 'Others')], default=False, max_length=1),
        ),
    ]