# Generated by Django 4.0.7 on 2022-09-22 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0035_remove_product_base_unit_unitexchange_is_base_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='customergroup',
            name='date_updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngày cập nhật'),
        ),
        migrations.AddField(
            model_name='customergroup',
            name='user_created',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customergroup',
            name='user_updated',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
