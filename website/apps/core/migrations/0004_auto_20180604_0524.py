# Generated by Django 2.0.1 on 2018-06-04 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180426_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='icon',
            field=models.ImageField(blank=True, upload_to='business_profile_imgs/'),
        ),
    ]
