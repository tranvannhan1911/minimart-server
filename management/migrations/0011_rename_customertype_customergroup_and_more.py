# Generated by Django 4.0.7 on 2022-08-27 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_alter_staff_phone_alter_staff_status_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerType',
            new_name='CustomerGroup',
        ),
        migrations.RenameField(
            model_name='promotion',
            old_name='applicable_customer_groups',
            new_name='applicable_customer_groups',
        ),
    ]