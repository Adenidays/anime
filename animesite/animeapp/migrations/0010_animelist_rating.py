# Generated by Django 4.2.5 on 2023-10-11 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animeapp', '0009_remove_animelist_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='animelist',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]
