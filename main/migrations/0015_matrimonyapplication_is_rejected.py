# Generated by Django 3.1.2 on 2020-12-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_receipt_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrimonyapplication',
            name='is_rejected',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Has been rejected?'),
        ),
    ]
