# Generated by Django 4.0.7 on 2022-09-06 15:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0044_alter_promotiondetail_applicable_product_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculationUnit',
            fields=[
                ('unit_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Mã đơn vị tính')),
                ('name', models.CharField(max_length=50, verbose_name='Tên đơn vị tính')),
            ],
            options={
                'db_table': 'CalculationUnit',
            },
        ),
        migrations.AddField(
            model_name='pricedetail',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Thời gian kết thúc'),
        ),
        migrations.AddField(
            model_name='pricedetail',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Thời gian bắt đầu'),
        ),
        migrations.AddField(
            model_name='pricelist',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='Tên bảng giá'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='description',
            field=models.TextField(default='', verbose_name='Mô tả chương trình khuyến mãi'),
        ),
        migrations.AddField(
            model_name='warehousetransaction',
            name='reference',
            field=models.CharField(max_length=30, null=True, verbose_name='Hóa đơn hoặc mã phiếu'),
        ),
        migrations.AlterField(
            model_name='inventoryreceivingvoucher',
            name='status',
            field=models.CharField(choices=[('pending', 'Chờ xác nhận'), ('complete', 'Hoàn thành'), ('cancel', 'Hủy')], max_length=15, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='applicable_customer_groups',
            field=models.ManyToManyField(db_table='ApplicableCustomerGroup', null=True, to='management.customergroup'),
        ),
        migrations.AlterField(
            model_name='promotionhistory',
            name='reduction_quantity',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='Số lượng sản phẩm được nhận'),
        ),
        migrations.RenameModel(
            old_name='Refund',
            new_name='OrderRefund',
        ),
        migrations.CreateModel(
            name='OrderRefundDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Số lượng')),
                ('note', models.TextField(verbose_name='Ghi chú')),
                ('order_refund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.orderrefund')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.product')),
                ('unit_exchange', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.unitexchange', verbose_name='Đơn vị tính')),
            ],
            options={
                'db_table': 'OrderRefundDetail',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='base_unit',
            field=models.ForeignKey(help_text='Đơn vị cơ bản', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.calculationunit', verbose_name='Đơn vị cơ bản'),
        ),
        migrations.AlterField(
            model_name='unitexchange',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unitexchanges', to='management.calculationunit'),
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]