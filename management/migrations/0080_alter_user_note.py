# Generated by Django 4.0.7 on 2022-11-22 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0079_alter_productgroup_product_group_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Ghi chú'),
        ),
    ]
