# Generated by Django 2.1.7 on 2019-02-25 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ro_operations', '0011_auto_20190219_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roleplayermanagement',
            name='created_date',
        ),
    ]
