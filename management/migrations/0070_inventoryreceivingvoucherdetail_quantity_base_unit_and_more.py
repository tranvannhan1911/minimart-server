# Generated by Django 4.0.7 on 2022-10-18 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0069_remove_pricedetail_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryreceivingvoucherdetail',
            name='quantity_base_unit',
            field=models.PositiveIntegerField(default=1, verbose_name='Số lượng trên đơn vị cơ bản'),
        ),
        migrations.AddField(
            model_name='inventoryreceivingvoucherdetail',
            name='unit_exchange',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='management.unitexchange', verbose_name='Đơn vị tính'),
            preserve_default=False,
        ),
    ]
