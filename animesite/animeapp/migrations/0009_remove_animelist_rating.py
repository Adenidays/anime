# Generated by Django 4.2.5 on 2023-10-11 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animeapp', '0008_animelist_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animelist',
            name='rating',
        ),
    ]
