# Generated by Django 4.1.4 on 2023-01-07 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_ads_author_alter_ads_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ads',
            name='address',
        ),
    ]