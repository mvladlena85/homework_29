# Generated by Django 4.1.4 on 2023-01-20 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_location_id_user_locations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]