# Generated by Django 4.2.5 on 2023-09-28 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_user_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_name',
        ),
    ]