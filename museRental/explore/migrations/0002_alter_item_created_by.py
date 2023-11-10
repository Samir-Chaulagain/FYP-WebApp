# Generated by Django 4.2.6 on 2023-11-10 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('explore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='accounts.user'),
        ),
    ]
