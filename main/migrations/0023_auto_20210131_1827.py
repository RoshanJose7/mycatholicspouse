# Generated by Django 3.1.2 on 2021-01-31 12:57

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20210114_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrimonyapplication',
            name='family_photo_1',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.get_photo_path),
        ),
        migrations.AddField(
            model_name='matrimonyapplication',
            name='passport_photo_1',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.get_photo_path),
        ),
        migrations.AddField(
            model_name='matrimonyapplication',
            name='your_photo_1_1',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.get_photo_path),
        ),
        migrations.AddField(
            model_name='matrimonyapplication',
            name='your_photo_2_1',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.get_photo_path),
        ),
        migrations.AddField(
            model_name='matrimonyapplication',
            name='your_photo_3_1',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.get_photo_path),
        ),
    ]