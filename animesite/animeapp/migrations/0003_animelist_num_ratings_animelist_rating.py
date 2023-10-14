# Generated by Django 4.2.5 on 2023-10-10 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animeapp', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='animelist',
            name='num_ratings',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='animelist',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
    ]