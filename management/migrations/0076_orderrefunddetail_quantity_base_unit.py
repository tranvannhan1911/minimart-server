# Generated by Django 4.0.7 on 2022-11-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0075_orderrefunddetail_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderrefunddetail',
            name='quantity_base_unit',
            field=models.PositiveIntegerField(default=0, verbose_name='Số lượng đơn vị tính cơ bản'),
        ),
    ]
