# Generated by Django 4.2.5 on 2023-10-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0008_remove_user_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='User Name'),
        ),
    ]
