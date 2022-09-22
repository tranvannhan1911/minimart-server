# Generated by Django 4.0.7 on 2022-09-22 03:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0031_alter_promotion_applicable_customer_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculationunit',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='customergroup',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='hierarchytree',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='inventoryreceivingvoucher',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='inventoryvoucher',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày lập hóa đơn'),
        ),
        migrations.AddField(
            model_name='orderrefund',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='pricelist',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='productgroup',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='unitexchange',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngày tạo'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='history',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='promotionhistory',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='warehousetransaction',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, serialize=False, verbose_name='Ngày tạo'),
        ),
    ]
