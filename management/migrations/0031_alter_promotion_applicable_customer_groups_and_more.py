# Generated by Django 4.0.7 on 2022-09-22 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0030_hierarchytree_note_history_note_pricedetail_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='applicable_customer_groups',
            field=models.ManyToManyField(blank=True, db_table='ApplicableCustomerGroup', to='management.customergroup'),
        ),
        migrations.AlterField(
            model_name='promotiondetail',
            name='applicable_product_groups',
            field=models.ManyToManyField(blank=True, db_table='ApplicableProductGroup', to='management.productgroup'),
        ),
        migrations.AlterField(
            model_name='promotiondetail',
            name='applicable_products',
            field=models.ManyToManyField(blank=True, db_table='ApplicableProduct', to='management.product'),
        ),
    ]