# Generated by Django 4.0.7 on 2022-08-27 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_remove_pricelist_price_remove_pricelist_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricedetail',
            name='price',
            field=models.FloatField(default=0, verbose_name='Giá bán'),
        ),
        migrations.AddField(
            model_name='pricedetail',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pricelists', to='management.product', verbose_name='Sản phẩm'),
        ),
        migrations.AddField(
            model_name='pricedetail',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pricelists', to='management.unit', verbose_name='Đơn vị tính'),
        ),
    ]
