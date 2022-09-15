# Generated by Django 4.0.7 on 2022-09-13 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_product_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='base_unit',
            field=models.ForeignKey(help_text='Đơn vị cơ bản', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='management.calculationunit', verbose_name='Đơn vị cơ bản'),
        ),
        migrations.AlterField(
            model_name='product',
            name='units',
            field=models.ManyToManyField(blank=True, through='management.UnitExchange', to='management.calculationunit'),
        ),
        migrations.AlterField(
            model_name='unitexchange',
            name='allow_sale',
            field=models.BooleanField(default=False, help_text='Cho phép bán hàng bằng đơn vị này không?', verbose_name='Đơn vị được phép bán hàng'),
        ),
        migrations.AlterField(
            model_name='unitexchange',
            name='value',
            field=models.PositiveIntegerField(default=1, help_text='Đơn vị này bằng bao nhiêu đơn vị mặc định?', verbose_name='Giá trị quy đổi'),
        ),
    ]