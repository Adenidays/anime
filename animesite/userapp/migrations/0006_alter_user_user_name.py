# Generated by Django 4.2.5 on 2023-09-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0005_alter_user_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='User Name'),
        ),
    ]
