# Generated by Django 2.2.2 on 2020-05-08 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20200506_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='dimension',
        ),
        migrations.RemoveField(
            model_name='product',
            name='primary_material',
        ),
    ]
