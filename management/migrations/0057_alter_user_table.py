# Generated by Django 4.0.7 on 2022-10-12 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0056_user_is_manager'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='Staff',
        ),
    ]
