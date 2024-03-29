# Generated by Django 4.0.7 on 2022-09-20 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0017_remove_inventoryreceivingvoucherdetail_unit_exchange_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hierarchytree',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='management.hierarchytree'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='applicable_customer_groups',
            field=models.ManyToManyField(db_table='ApplicableCustomerGroup', null=True, to='management.customergroup'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='image',
            field=models.CharField(max_length=255, null=True, verbose_name='Hình ảnh'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Trạng thái'),
        ),
    ]
