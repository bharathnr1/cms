# Generated by Django 2.2.2 on 2020-05-09 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200509_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='primarymaterial',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Product'),
        ),
    ]
