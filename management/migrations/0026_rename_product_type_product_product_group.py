# Generated by Django 4.0.7 on 2022-08-27 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0025_hierarchytree_parent_alter_hierarchytree_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_type',
            new_name='product_group',
        ),
    ]
