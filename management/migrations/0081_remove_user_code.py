# Generated by Django 4.0.7 on 2022-11-22 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0080_alter_user_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='code',
        ),
    ]
