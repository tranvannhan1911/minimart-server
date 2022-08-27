# Generated by Django 4.0.7 on 2022-08-27 14:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0018_alter_pricedetail_table_alter_promotionhistory_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 37, 34, 696357, tzinfo=utc), verbose_name='Ngày lập hóa đơn'),
        ),
        migrations.AddField(
            model_name='promotionhistory',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 37, 34, 714600, tzinfo=utc), verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='refund',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 37, 34, 708769, tzinfo=utc), verbose_name='Ngày trả hàng'),
        ),
        migrations.AddField(
            model_name='warehousetransaction',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 37, 34, 711032, tzinfo=utc), verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='inventoryreceivingvoucher',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 37, 34, 709283, tzinfo=utc), verbose_name='Ngày nhập hàng'),
        ),
        migrations.AlterField(
            model_name='inventoryvoucher',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 14, 37, 34, 710142, tzinfo=utc), verbose_name='Ngày tạo phiếu kiểm kê'),
        ),
    ]