# Generated by Django 4.0.7 on 2022-09-11 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_customergroup_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.CharField(max_length=50, null=True, verbose_name='Địa chỉ email'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='note',
            field=models.TextField(help_text='Ghi chú nội bộ', null=True, verbose_name='Ghi chú'),
        ),
        migrations.AlterField(
            model_name='user',
            name='customer_group',
            field=models.ManyToManyField(blank=True, db_table='CustomerGroupDetail', related_name='customer_group_detail', to='management.customergroup'),
        ),
    ]