# Generated by Django 4.0.7 on 2022-11-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0077_unitexchange_is_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(max_length=15, unique=True, verbose_name='Mã sản phẩm'),
        ),
    ]