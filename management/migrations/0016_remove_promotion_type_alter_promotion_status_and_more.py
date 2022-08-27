# Generated by Django 4.0.7 on 2022-08-27 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0015_pricedetail_price_pricedetail_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='type',
        ),
        migrations.AlterField(
            model_name='promotion',
            name='status',
            field=models.BooleanField(verbose_name='Trạng thái'),
        ),
        migrations.CreateModel(
            name='PromotionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Product', 'Tặng sản phẩm'), ('Percent', 'Giảm số tiền theo % hóa đơn'), ('Fixed', 'Giảm số tiền được định trước')], max_length=15, verbose_name='Loại khuyến mãi')),
                ('reduction_amount', models.FloatField(null=True, verbose_name='Số tiền được giảm')),
                ('fixed_voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.promotionfixedvoucher')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.order')),
                ('order_detail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.orderdetail')),
                ('percent_voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.promotionpercentvoucher')),
                ('product_voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.promotionproductvoucher')),
            ],
        ),
    ]