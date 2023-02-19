# Generated by Django 4.1.5 on 2023-02-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0004_order_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='time',
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
