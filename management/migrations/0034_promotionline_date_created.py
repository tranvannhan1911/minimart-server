# Generated by Django 4.0.7 on 2022-09-22 03:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0033_alter_calculationunit_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionline',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngày tạo'),
        ),
    ]
