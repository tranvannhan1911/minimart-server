# Generated by Django 4.0.7 on 2022-09-30 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0047_rename_reduction_amount_promotionhistory_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.pricedetail'),
        ),
        migrations.AlterField(
            model_name='warehousetransaction',
            name='type',
            field=models.CharField(choices=[('order', 'Bán hàng'), ('promotion', 'Khuyến mãi'), ('inventory', 'Kiểm kê'), ('inventory_cancel', 'Hủy kiểm kê'), ('inventory_receiving', 'Nhập hàng'), ('inventory_receiving_cancel', 'Hủy nhập hàng'), ('refund', 'Trả hàng')], max_length=30, verbose_name='Loại biến động'),
        ),
    ]
