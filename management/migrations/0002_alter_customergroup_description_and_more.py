# Generated by Django 4.0.7 on 2022-09-08 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customergroup',
            name='description',
            field=models.TextField(blank=True, verbose_name='Mô tả nhóm khách hàng'),
        ),
        migrations.AlterField(
            model_name='promotiondetail',
            name='promotion_code',
            field=models.CharField(max_length=15, null=True, unique=True, verbose_name='Mã khuyến mãi'),
        ),
        migrations.AlterField(
            model_name='user',
            name='customer_group',
            field=models.ManyToManyField(blank=True, db_table='CustomerGroupDetail', to='management.customergroup'),
        ),
    ]