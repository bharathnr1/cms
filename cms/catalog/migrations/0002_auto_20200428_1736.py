# Generated by Django 2.2.1 on 2020-04-28 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='height',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='length',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='width',
            field=models.IntegerField(),
        ),
    ]
