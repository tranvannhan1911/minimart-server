# Generated by Django 4.0.7 on 2022-10-12 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0055_remove_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='Quản lý'),
        ),
    ]
