# Generated by Django 4.0.6 on 2022-11-06 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_rest_city_remove_rest_drive_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rest',
            old_name='restaraunt',
            new_name='rest',
        ),
    ]