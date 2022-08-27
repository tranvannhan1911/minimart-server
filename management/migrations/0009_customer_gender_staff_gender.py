# Generated by Django 4.0.7 on 2022-08-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_alter_customer_customer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('M', 'Nam'), ('F', 'Nữ'), ('U', 'Không xác định')], default='U', max_length=1, verbose_name='Giới tính'),
        ),
        migrations.AddField(
            model_name='staff',
            name='gender',
            field=models.CharField(choices=[('M', 'Nam'), ('F', 'Nữ'), ('U', 'Không xác định')], default='U', max_length=1, verbose_name='Giới tính'),
        ),
    ]