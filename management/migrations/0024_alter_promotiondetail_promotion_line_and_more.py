# Generated by Django 4.0.7 on 2022-09-21 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0023_customer_is_active_customer_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotiondetail',
            name='promotion_line',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='management.promotionline'),
        ),
        migrations.AlterField(
            model_name='promotionline',
            name='promotion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='management.promotion'),
        ),
    ]