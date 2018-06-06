# Generated by Django 2.0.1 on 2018-06-04 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_remove_inventory_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storelocation',
            name='offers',
        ),
        migrations.AddField(
            model_name='inventory',
            name='location',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='item.StoreLocation'),
        ),
    ]