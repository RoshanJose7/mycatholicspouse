# Generated by Django 3.1.2 on 2020-11-21 13:40

import cloudinary.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MatrimonyApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(blank=True, default=False, null=True, verbose_name='Has been approved?')),
                ('first_name', models.CharField(default='', max_length=40)),
                ('middle_name', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('last_name', models.CharField(default='', max_length=40)),
                ('mother_tongue', models.CharField(blank=True, choices=[('English', 'English'), ('Assamese', 'Assamese'), ('Bengali', 'Bengali'), ('Gujarati', 'Gujarati'), ('Hindi', 'Hindi'), ('Kannada', 'Kannada'), ('Kashmiri', 'Kashmiri'), ('Konkani', 'Konkani'), ('Malayalam', 'Malayalam'), ('Manipuri', 'Manipuri'), ('Marathi', 'Marathi'), ('Nepali', 'Nepali'), ('Oriya', 'Oriya'), ('Punjabi', 'Punjabi'), ('Sanskrit', 'Sanskrit'), ('Sindhi', 'Sindhi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu'), ('Urdu', 'Urdu'), ('Bodo', 'Bodo'), ('Santhali', 'Santhali'), ('Maithili', 'Maithili'), ('Dogri', 'Dogri')], default='English', max_length=20, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=10, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('addr_1', models.TextField(default='', verbose_name='Address Line 1')),
                ('addr_2', models.TextField(blank=True, default='', verbose_name='Address Line 2')),
                ('city', models.CharField(default='', max_length=40)),
                ('state', models.CharField(default='', max_length=40)),
                ('country', models.CharField(default='', max_length=40)),
                ('pin_code', models.CharField(default='', max_length=8)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('education_level', models.CharField(blank=True, choices=[('Less Than 10th', 'Less Than 10th'), ('10th', '10th'), ('12th', '12th'), ('Graduate', 'Graduate'), ('Post Graduate', 'Post Graduate'), ('Other', 'Other')], default='Less Than 10th', max_length=30, null=True, verbose_name='Education')),
                ('tenth_marks', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='10th Marks (in %)')),
                ('hs_marks', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='12th Marks (in %)')),
                ('grad_marks', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Graduate Marks (in %)')),
                ('post_grad_marks', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Post Graduate Marks (in %)')),
                ('other_marks', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Other Marks (in %)')),
                ('tenth_school', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='School')),
                ('hs_school', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='School/College')),
                ('grad_school', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='College/University')),
                ('post_grad_school', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='College/University')),
                ('other_school', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='College/University')),
                ('other_type', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Degree Type')),
                ('height', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True, verbose_name='Height (Cms)')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True, verbose_name='Weight (Kgs)')),
                ('date_of_birth', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date of Birth')),
                ('place_of_birth', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Place of Birth')),
                ('parish_baptized_at', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Parish Baptized at')),
                ('present_parish', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Present Parish')),
                ('diocese', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Diocese')),
                ('rite', models.CharField(blank=True, choices=[('Latin', 'Latin'), ('Syro Malabar', 'Syro Malabar'), ('Syro Malankara', 'Syro Malankara'), ('Other', 'Other')], default='Latin', max_length=30, null=True)),
                ('diet', models.CharField(blank=True, choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian')], default='Vegetarian', max_length=30, null=True, verbose_name='Diet')),
                ('smoke', models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes'), ('Occasionally', 'Occasionally')], default='No', max_length=30, null=True, verbose_name='Smoke')),
                ('drink', models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes'), ('Occasionally', 'Occasionally')], default='No', max_length=30, null=True, verbose_name='Drink')),
                ('health_issues', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=30, null=True, verbose_name='Health Issues (if any)')),
                ('health_issues_details', models.TextField(blank=True, null=True, verbose_name='Health Issues (Details)')),
                ('occupation', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Occupation')),
                ('place_of_employment', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Place of Employment')),
                ('designation', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Designation')),
                ('years_of_employment', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Years of Employment')),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True, verbose_name='Annual Income')),
                ('other_income', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Any Other Income')),
                ('about_yourself', models.TextField(blank=True, default='', null=True, verbose_name='More details about yourself')),
                ('marital_status', models.CharField(blank=True, choices=[('Single', 'Single'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], default='Single', max_length=50, null=True, verbose_name='Marital Status')),
                ('disability', models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes')], default='No', max_length=4, null=True, verbose_name='Disability')),
                ('disability_type', models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='Disability Type')),
                ('former_spouse_name_1', models.CharField(blank=True, default='', max_length=100, verbose_name='Former Spouse Name')),
                ('marriage_date_1', models.DateField(blank=True, default=datetime.datetime(1970, 1, 1, 5, 30), null=True, verbose_name='Marriage Date')),
                ('divorce_date', models.DateField(blank=True, default=datetime.datetime(1970, 1, 1, 5, 30), null=True, verbose_name='Divorce Date')),
                ('marriage_annulment_date', models.DateField(blank=True, default=datetime.datetime(1970, 1, 1, 5, 30), null=True, verbose_name='Marriage Annulment Date')),
                ('no_of_children_1', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No. of children from this marriage (if any)')),
                ('no_of_sons_1', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No. of sons from this marriage (if any)')),
                ('no_of_daughters_1', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No. of daughters from this marriage (if any)')),
                ('additional_details', models.TextField(blank=True, default='', null=True, verbose_name='Additional Details (optional)')),
                ('former_spouse_name_2', models.CharField(blank=True, default='', max_length=100, verbose_name='Former Spouse Name')),
                ('marriage_date_2', models.DateField(blank=True, default=datetime.datetime(1970, 1, 1, 5, 30), null=True, verbose_name='Marriage Date')),
                ('date_of_death', models.DateField(blank=True, default=datetime.datetime(1970, 1, 1, 5, 30), null=True, verbose_name='Date of Death of former spouse')),
                ('no_of_children_2', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No. of children from this marriage (if any)')),
                ('no_of_sons_2', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No. of sons from this marriage (if any)')),
                ('no_of_daughters_2', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No. of daughters from this marriage (if any)')),
                ('cause_of_death', models.TextField(blank=True, default='', null=True, verbose_name='Cause of death of former spouse (optional)')),
                ('fathers_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name="Father's Name")),
                ('mothers_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name="Mother's Name")),
                ('siblings', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Siblings (Brothers & Sisters)')),
                ('brothers', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Brothers')),
                ('sisters', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Sisters')),
                ('values', models.CharField(blank=True, choices=[('Traditional', 'Traditional'), ('Moderate', 'Moderate'), ('Liberal', 'Liberal')], default='Traditional', max_length=30, null=True, verbose_name='Family Values')),
                ('family_members', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Family members residing at your Residence')),
                ('about_family', models.TextField(blank=True, default='', null=True, verbose_name='More details about Family')),
                ('lower_age', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Lower Age Bound')),
                ('upper_age', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Upper Age Bound')),
                ('language', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Language')),
                ('place_of_residence', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Language')),
                ('education', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Education')),
                ('employment', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Employmnent')),
                ('salary_lower', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True, verbose_name='Salary')),
                ('salary_upper', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True, verbose_name='Salary')),
                ('special_needs', models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes'), ('No Preference', 'No Preference')], default='No', max_length=20, null=True)),
                ('widowed', models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes'), ('No Preference', 'No Preference')], default='No', max_length=20, null=True)),
                ('community', models.CharField(blank=True, choices=[('Latin', 'Latin'), ('Syro Malabar', 'Syro Malabar'), ('Syro Malankara', 'Syro Malankara'), ('Other', 'Other'), ('No Preference', 'No Preference')], default='Latin', max_length=30, null=True)),
                ('family_values', models.CharField(blank=True, choices=[('Traditional', 'Traditional'), ('Moderate', 'Moderate'), ('Liberal', 'Liberal'), ('No Preference', 'No Preference')], default='Traditional', max_length=30, null=True, verbose_name='Family Values / Background')),
                ('passport_photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='passport_photo')),
                ('family_photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='family_photo')),
                ('your_photo_1', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='your_photo_1')),
                ('your_photo_2', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='your_photo_2')),
                ('your_photo_3', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='your_photo_3')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
