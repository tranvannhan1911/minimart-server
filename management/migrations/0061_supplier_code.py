# Generated by Django 4.0.7 on 2022-10-16 16:36

from django.db import migrations, models

import management


def random_code(apps, schema_editor):
    for i in management.models.Supplier.objects.all():
        i.code=management.models.unique_rand()
        i.save()
        
class Migration(migrations.Migration):

    dependencies = [
        ('management', '0060_alter_user_code_alter_counterindex_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='code',
            field=models.CharField(default="", max_length=10, verbose_name='Mã code'),
        ),
        migrations.RunPython(random_code),
        migrations.AlterField(
            model_name='supplier',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='Mã code'),
        ),
    ]
