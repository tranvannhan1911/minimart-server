# Generated by Django 4.0.7 on 2022-09-03 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0035_history'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='history',
            table='History',
        ),
        migrations.AlterModelTable(
            name='unitexchange',
            table='UnitExchange',
        ),
    ]
