# Generated by Django 3.1.2 on 2020-12-27 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_matrimonyapplication_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrimonyapplication',
            name='disability_type',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Disability Type'),
        ),
    ]