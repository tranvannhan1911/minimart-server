# Generated by Django 4.0.7 on 2022-10-16 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0058_counterindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(default='', max_length=10, verbose_name='Mã nhân viên'),
            preserve_default=False,
        ),
    ]
