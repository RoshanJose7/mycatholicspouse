# Generated by Django 3.1.2 on 2020-12-20 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20201220_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='order_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
