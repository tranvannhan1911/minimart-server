# Generated by Django 4.0.7 on 2022-09-20 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_remove_user_customer_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_group',
            field=models.ManyToManyField(blank=True, db_table='CustomerGroupDetail', related_name='customer_group_detail', to='management.customergroup'),
        ),
    ]
