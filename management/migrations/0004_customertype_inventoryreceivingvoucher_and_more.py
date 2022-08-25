# Generated by Django 4.0.7 on 2022-08-25 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_customer_order_pricelist_product_producttype_staff_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tên nhóm khách hàng')),
                ('description', models.TextField(verbose_name='Mô tả nhóm khách hàng')),
                ('note', models.TextField(blank=True, verbose_name='Ghi chú')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryReceivingVoucher',
            fields=[
                ('voucher_id', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Mã phiếu nhập hàng')),
                ('date_created', models.DateTimeField(verbose_name='Thời gian tạo')),
                ('status', models.CharField(max_length=15, verbose_name='Trạng thái')),
                ('note', models.TextField(verbose_name='Ghi chú')),
                ('total', models.FloatField(verbose_name='Thành tiền')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryVoucher',
            fields=[
                ('voucher_id', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Mã phiếu kiểm kê')),
                ('date_created', models.DateTimeField(verbose_name='Thời gian tạo')),
                ('status', models.CharField(max_length=15, verbose_name='Trạng thái')),
                ('note', models.TextField(verbose_name='Ghi chú')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_code', models.CharField(max_length=15, verbose_name='Mã khuyến mãi')),
                ('title', models.CharField(max_length=255, verbose_name='Tiêu đề của chương trình khuyến mãi')),
                ('image', models.CharField(max_length=255, verbose_name='Hình ảnh')),
                ('start_date', models.DateTimeField(verbose_name='Thời gian bắt đầu áp dụng')),
                ('end_date', models.DateTimeField(verbose_name='Thời gian kết thúc')),
                ('type', models.CharField(choices=[('Product', 'Tặng sản phẩm'), ('Percent', 'Giảm số tiền theo % hóa đơn'), ('Fixed', 'Giảm số tiền được định trước')], max_length=15, verbose_name='Loại khuyến mãi')),
                ('status', models.CharField(max_length=15, verbose_name='Trạng thái')),
                ('max_quantity', models.IntegerField(verbose_name='Số lần áp dụng tối đa')),
                ('max_quantity_per_customer', models.IntegerField(verbose_name='Số lần áp dụng tối đa trên khách hàng')),
                ('max_quantity_per_customer_per_day', models.IntegerField(verbose_name='Số lần áp dụng tối đa trên khách hàng trên 1 ngày')),
                ('applicable_customer_types', models.ManyToManyField(db_table='ApplicableCustomerType', to='management.customertype')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
        migrations.AddField(
            model_name='order',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.staff'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='management.customer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='management.producttype'),
        ),
        migrations.CreateModel(
            name='PromotionProductVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_buy', models.PositiveIntegerField(verbose_name='Số lượng sản phẩm cần mua')),
                ('quantity_received', models.PositiveIntegerField(verbose_name='Số lượng sản phẩm được nhận')),
                ('applicable_product_types', models.ManyToManyField(db_table='ApplicableProductType', to='management.producttype')),
                ('applicable_products', models.ManyToManyField(db_table='ApplicableProduct', to='management.product')),
                ('promotion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='management.promotion')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionPercentVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_total', models.FloatField(verbose_name='Số tiền tối thiểu trên hóa đơn')),
                ('percent', models.FloatField(verbose_name='Phần trăm giảm giá')),
                ('maximum_reduction_amount', models.FloatField(verbose_name='Số tiền được giảm tối đa')),
                ('promotion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='management.promotion')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionFixedVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_total', models.FloatField(verbose_name='Số tiền tối thiểu trên hóa đơn')),
                ('reduction_amount', models.FloatField(verbose_name='Số tiền được giảm')),
                ('promotion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='management.promotion')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Số lượng')),
                ('total', models.FloatField(verbose_name='Thành tiền')),
                ('note', models.TextField(verbose_name='Ghi chú')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.order')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.pricelist')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.product')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryVoucherDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_before', models.PositiveIntegerField(verbose_name='Số lượng trước')),
                ('quantity_after', models.PositiveIntegerField(verbose_name='Số lượng sau')),
                ('note', models.TextField(verbose_name='Ghi chú')),
                ('inventory_voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.inventoryvoucher')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.unit')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryReceivingVoucherDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Số lượng')),
                ('price', models.FloatField(verbose_name='Giá nhập')),
                ('note', models.TextField(verbose_name='Ghi chú')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.product')),
                ('receiving_voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.inventoryreceivingvoucher')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.supplier')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.unit')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.customertype'),
        ),
    ]