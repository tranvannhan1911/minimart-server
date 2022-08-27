# Generated by Django 4.0.7 on 2022-08-27 14:49

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_order_date_created_promotionhistory_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryreceivingvoucherdetail',
            name='supplier',
        ),
        migrations.AddField(
            model_name='inventoryreceivingvoucher',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.supplier'),
        ),
        migrations.AlterField(
            model_name='inventoryreceivingvoucher',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 49, 4, 861440, tzinfo=utc), verbose_name='Ngày nhập hàng'),
        ),
        migrations.AlterField(
            model_name='inventoryvoucher',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 49, 4, 862454, tzinfo=utc), verbose_name='Ngày tạo phiếu kiểm kê'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 49, 4, 848686, tzinfo=utc), verbose_name='Ngày lập hóa đơn'),
        ),
        migrations.AlterField(
            model_name='promotionhistory',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 49, 4, 866941, tzinfo=utc), verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='refund',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 49, 4, 860755, tzinfo=utc), verbose_name='Ngày trả hàng'),
        ),
        migrations.AlterField(
            model_name='warehousetransaction',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 49, 4, 863330, tzinfo=utc), verbose_name='Ngày tạo'),
        ),
    ]