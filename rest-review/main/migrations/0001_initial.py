# Generated by Django 4.0.6 on 2022-10-30 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(db_index=True, max_length=255)),
                ('restaraunt', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('category', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=50)),
                ('drive_time', models.IntegerField()),
                ('notes', models.TextField()),
            ],
        ),
    ]
