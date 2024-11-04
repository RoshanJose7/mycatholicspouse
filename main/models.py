from django.db import models
from django.core import files
from django.utils import timezone
from django.contrib.auth.models import User

import datetime
import requests
from io import BytesIO
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField

lang_list = [
    'Assamese', 'Bengali', 'Gujarati', 'Hindi', 'Kannada', 'Kashmiri', 'Konkani', 'Malayalam',
    'Manipuri', 'Marathi', 'Nepali', 'Oriya', 'Punjabi', 'Sanskrit', 'Sindhi', 'Tamil', 'Telugu',
    'Urdu', 'Bodo', 'Santhali', 'Maithili', 'Dogri', 'English',
]

lang_choices = (
    ('English', 'English'),
    ('Assamese', 'Assamese'),
    ('Bengali', 'Bengali'),
    ('Gujarati', 'Gujarati'),
    ('Hindi', 'Hindi'),
    ('Kannada', 'Kannada'),
    ('Kashmiri', 'Kashmiri'),
    ('Konkani', 'Konkani'),
    ('Malayalam', 'Malayalam'),
    ('Manipuri', 'Manipuri'),
    ('Marathi', 'Marathi'),
    ('Nepali', 'Nepali'),
    ('Oriya', 'Oriya'),
    ('Punjabi', 'Punjabi'),
    ('Sanskrit', 'Sanskrit'),
    ('Sindhi', 'Sindhi'),
    ('Tamil', 'Tamil'),
    ('Telugu', 'Telugu'),
    ('Urdu', 'Urdu'),
    ('Bodo', 'Bodo'),
    ('Santhali', 'Santhali'),
    ('Maithili', 'Maithili'),
    ('Dogri', 'Dogri'),
)


class PasswordResetToken(models.Model):
    token = models.TextField(default="", blank=True, null=True)
    email = models.CharField(max_length=60, default="User Email", blank=True, null=True)

    def __str__(self):
        return self.email


class Connection(models.Model):
    user = models.CharField(max_length=100, null=True,
                            verbose_name="User Email", unique=True)
    has_liked = models.ManyToManyField(User, related_name="user_has_liked", blank=True)
    was_liked = models.ManyToManyField(User, related_name="user_was_liked_by", blank=True)
    has_unliked = models.ManyToManyField(User, related_name="user_has_unliked", blank=True)
    was_unliked = models.ManyToManyField(User, related_name="user_was_unliked_by", blank=True)
    matched = models.ManyToManyField(
        User, related_name="user_has_matched_with", blank=True)
    has_blocked = models.ManyToManyField(User, related_name="has_blocked", blank=True)
    was_blocked = models.ManyToManyField(User, related_name="was_blocked", blank=True)

    def __str__(self):
        return self.user


# Create your models here.
class Plan(models.Model):
    plan_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Plan Name", unique=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    price = models.DecimalField(verbose_name="Price", max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.plan_name


def get_photo_path(instance, filename) -> str:
    """
        get user photo file path.
    """
    return f"{instance.email}/{filename}"


class MatrimonyApplication(models.Model):
    # operational
    subs_start = models.DateTimeField(verbose_name="Subscription Start Date", default=timezone.now, blank=True,
                                      null=True)
    subs_end = models.DateTimeField(verbose_name="Subscription End Date", default=timezone.now, blank=True, null=True)

    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    migrated = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # Change to models.CASCADE later
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(
        verbose_name="Has been approved?", default=False, blank=True, null=True)
    is_rejected = models.BooleanField(
        verbose_name="Has been rejected?", default=False, blank=True, null=True)
    is_settled = models.BooleanField(verbose_name="Has settled?", default=False, blank=True, null=True)
    connection = models.OneToOneField(
        Connection, on_delete=models.SET_NULL, blank=True, null=True)
    reg_id = models.CharField(max_length=20, blank=True, null=True)
    interim_password = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=30, choices=(
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Blocked", "Blocked"),
    ), default="Active", blank=True, null=True)
    is_blocked = models.BooleanField(
        verbose_name="Has been blocked by admin?", default=False, blank=True, null=True)
    is_paid = models.BooleanField(verbose_name="Is Paid User?", default=False, blank=True, null=True)

    # primary_details
    first_name = models.CharField(max_length=40, default="")
    middle_name = models.CharField(
        max_length=40, default="", blank=True, null=True)
    last_name = models.CharField(max_length=40, default="")
    mother_tongue = models.CharField(
        max_length=20, default="English", choices=lang_choices, blank=True, null=True)
    gender = models.CharField(max_length=10,
                              default="Other",
                              choices=(
                                  ("Male", "Male"),
                                  ("Female", "Female"),
                                  ("Other", "Other"),
                              ), null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    addr_1 = models.TextField(
        verbose_name="Address Line 1", default='', null=True, blank=True)
    addr_2 = models.TextField(
        verbose_name="Address Line 2", default='', null=True, blank=True)
    city = models.CharField(max_length=40, default="", null=True, blank=True)
    state = models.CharField(max_length=40, default="", null=True, blank=True)
    country = models.CharField(max_length=40, default="", null=True, blank=True)
    pin_code = models.CharField(max_length=8, default="", blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    # educational_details
    education_level = models.CharField(max_length=30, verbose_name="Education", default="Less Than 10th",
                                       choices=(
                                           ("Less Than 10th", "Less Than 10th"),
                                           ("10th", "10th"),
                                           ("12th", "12th"),
                                           ("Graduate", "Graduate"),
                                           ("Post Graduate", "Post Graduate"),
                                           ("Other", "Other"),
                                       ), null=True, blank=True)
    tenth_marks = models.DecimalField(
        verbose_name="10th Marks (in %)", default=0, decimal_places=2, max_digits=5, blank=True, null=True)
    hs_marks = models.DecimalField(verbose_name="12th Marks (in %)",
                                   default=0, decimal_places=2, max_digits=5, blank=True, null=True)
    grad_marks = models.DecimalField(verbose_name="Graduate Marks (in %)",
                                     default=0, decimal_places=2, max_digits=5, blank=True, null=True)
    post_grad_marks = models.DecimalField(
        verbose_name="Post Graduate Marks (in %)", default=0, decimal_places=2, max_digits=5, blank=True, null=True)
    other_marks = models.DecimalField(
        verbose_name="Other Marks (in %)", default=0, decimal_places=2, max_digits=5, blank=True, null=True)

    tenth_school = models.CharField(
        max_length=100, default='', verbose_name="School", blank=True, null=True)
    hs_school = models.CharField(
        max_length=100, default='', verbose_name="School/College", blank=True, null=True)
    grad_school = models.CharField(
        max_length=100, default='', verbose_name="College/University", blank=True, null=True)
    post_grad_school = models.CharField(
        max_length=100, default='', verbose_name="College/University", blank=True, null=True)
    other_school = models.CharField(

        max_length=100, default='', verbose_name="College/University", blank=True, null=True)

    other_type = models.CharField(
        max_length=100, default='', verbose_name="Degree Type", blank=True, null=True)

    # personal_details
    height = models.DecimalField(verbose_name="Height (Cms)", default=0.0,
                                 decimal_places=2, max_digits=5, blank=True, null=True)
    weight = models.DecimalField(verbose_name="Weight (Kgs)", default=0.0,
                                 decimal_places=2, max_digits=5, blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", null=True, blank=True, default=timezone.now)
    place_of_birth = models.CharField(
        max_length=100, default="", verbose_name="Place of Birth", blank=True, null=True)
    parish_baptized_at = models.CharField(
        max_length=100, default="", verbose_name="Parish Baptized at", blank=True, null=True)
    present_parish = models.CharField(
        max_length=100, default="", verbose_name="Present Parish", blank=True, null=True)
    diocese = models.CharField(
        max_length=100, default="", verbose_name="Diocese", blank=True, null=True)
    rite = models.CharField(max_length=30, default="Latin",
                            choices=(
                                ("Latin", "Latin"),
                                ("Syro Malabar", "Syro Malabar"),
                                ("Syro Malankara", "Syro Malankara"),
                                ("Other", "Other"),
                            ), null=True, blank=True, )
    diet = models.CharField(max_length=30, verbose_name="Diet", default="Vegetarian",
                            choices=(
                                ("Vegetarian", "Vegetarian"),
                                ("Non-Vegetarian", "Non-Vegetarian"),
                            ), null=True, blank=True, )
    smoke = models.CharField(max_length=30, verbose_name="Smoke", default="No",
                             choices=(
                                 ("No", "No"),
                                 ("Yes", "Yes"),
                                 ("Occasionally", "Occasionally"),
                             ), null=True, blank=True, )
    drink = models.CharField(max_length=30, verbose_name="Drink", default="No",
                             choices=(
                                 ("No", "No"),
                                 ("Yes", "Yes"),
                                 ("Occasionally", "Occasionally"),
                             ), null=True, blank=True, )
    health_issues = models.CharField(max_length=30, verbose_name="Health Issues (if any)", default="No",
                                     choices=(
                                         ("Yes", "Yes"),
                                         ("No", "No"),
                                     ), null=True, blank=True)
    health_issues_details = models.TextField(
        blank=True, null=True, verbose_name="Health Issues (Details)")
    occupation = models.CharField(
        max_length=100, default='', verbose_name="Occupation", null=True, blank=True, )
    place_of_employment = models.CharField(
        max_length=100, default='', verbose_name="Place of Employment", null=True, blank=True, )
    designation = models.CharField(
        max_length=100, default='', verbose_name="Designation", null=True, blank=True, )
    years_of_employment = models.CharField(
        max_length=100, default='', verbose_name="Years of Employment", null=True, blank=True, )
    annual_income = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.0, verbose_name="Annual Income", null=True, blank=True, )
    other_income = models.CharField(
        max_length=100, default='', verbose_name="Any Other Income", null=True, blank=True, )
    about_yourself = models.TextField(
        verbose_name="More details about yourself", default='', null=True, blank=True, )
    marital_status = models.CharField(max_length=50, verbose_name="Marital Status", default='Single', choices=(
        ("Single", "Single"),
        ("Divorced", "Divorced"),
        ("Widowed", "Widowed"),
    ), null=True, blank=True, )
    disability = models.CharField(verbose_name="Disability", default='No', max_length=4, choices=(
        ("No", "No"),
        ("Yes", "Yes"),
    ), null=True, blank=True, )
    disability_type = models.TextField(
        verbose_name="Disability Type", null=True, blank=True, default='')

    # divorced
    former_spouse_name_1 = models.CharField(
        max_length=100, default='', verbose_name="Former Spouse Name", blank=True)
    marriage_date_1 = models.DateField(
        verbose_name="Marriage Date", null=True, blank=True, default=datetime.datetime.fromtimestamp(0))
    divorce_date = models.DateField(
        verbose_name="Divorce Date", null=True, blank=True, default=datetime.datetime.fromtimestamp(0))
    marriage_annulment_date = models.DateField(
        verbose_name="Marriage Annulment Date", null=True, blank=True, default=datetime.datetime.fromtimestamp(0))
    no_of_children_1 = models.PositiveIntegerField(
        verbose_name="No. of children from this marriage (if any)", null=True, blank=True, default=0)
    no_of_sons_1 = models.PositiveIntegerField(
        verbose_name="No. of sons from this marriage (if any)", null=True, blank=True, default=0)
    no_of_daughters_1 = models.PositiveIntegerField(
        verbose_name="No. of daughters from this marriage (if any)", null=True, blank=True, default=0)
    additional_details = models.TextField(
        verbose_name="Additional Details (optional)", default='', null=True, blank=True)

    # widowed
    former_spouse_name_2 = models.CharField(
        max_length=100, default='', verbose_name="Former Spouse Name", blank=True)
    marriage_date_2 = models.DateField(
        verbose_name="Marriage Date", null=True, blank=True, default=datetime.datetime.fromtimestamp(0))
    date_of_death = models.DateField(verbose_name="Date of Death of former spouse",
                                     null=True, blank=True, default=datetime.datetime.fromtimestamp(0))
    no_of_children_2 = models.PositiveIntegerField(
        verbose_name="No. of children from this marriage (if any)", null=True, blank=True, default=0)
    no_of_sons_2 = models.PositiveIntegerField(
        verbose_name="No. of sons from this marriage (if any)", null=True, blank=True, default=0)
    no_of_daughters_2 = models.PositiveIntegerField(
        verbose_name="No. of daughters from this marriage (if any)", null=True, blank=True, default=0)
    cause_of_death = models.TextField(
        verbose_name="Cause of death of former spouse (optional)", default='', null=True, blank=True)

    # family_details
    fathers_name = models.CharField(
        max_length=100, default='', verbose_name="Father's Name", blank=True, null=True)
    mothers_name = models.CharField(
        max_length=100, default='', verbose_name="Mother's Name", blank=True, null=True)
    siblings = models.PositiveSmallIntegerField(
        verbose_name="Siblings (Brothers & Sisters)", blank=True, null=True, default=0)
    brothers = models.PositiveSmallIntegerField(
        verbose_name="Brothers", blank=True, null=True, default=0)
    sisters = models.PositiveSmallIntegerField(
        verbose_name="Sisters", blank=True, null=True, default=0)
    values = models.CharField(max_length=30, verbose_name="Family Values", default="Traditional",
                              choices=(
                                  ("Traditional", "Traditional"),
                                  ("Moderate", "Moderate"),
                                  ("Liberal", "Liberal"),
                              ), null=True, blank=True, )
    family_members = models.PositiveSmallIntegerField(
        verbose_name="Family members residing at your Residence", blank=True, null=True, default=0)
    about_family = models.TextField(
        verbose_name="More details about Family", blank=True, null=True, default='')

    # partner_preference
    lower_age = models.PositiveIntegerField(
        default=0, verbose_name="Lower Age Bound", blank=True, null=True)
    upper_age = models.PositiveIntegerField(
        default=0, verbose_name="Upper Age Bound", blank=True, null=True)
    language = models.CharField(
        max_length=100, default='', verbose_name="Language", blank=True, null=True)
    place_of_residence = models.CharField(
        max_length=100, default='', verbose_name="Language", blank=True, null=True)
    education = models.CharField(
        max_length=100, default='', verbose_name="Education", blank=True, null=True)
    employment = models.CharField(
        max_length=100, default='', verbose_name="Employmnent", blank=True, null=True)
    salary_lower = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.0, verbose_name="Salary", blank=True, null=True)
    salary_upper = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.0, verbose_name="Salary", blank=True, null=True)
    special_needs = models.CharField(max_length=20, default="No", choices=(
        ("No", "No"),
        ("Yes", "Yes"),
        ("No Preference", "No Preference"),
    ), null=True, blank=True, )
    widowed = models.CharField(max_length=20, default="No", choices=(
        ("No", "No"),
        ("Yes", "Yes"),
        ("No Preference", "No Preference"),
    ), null=True, blank=True, )
    community = models.CharField(max_length=30, default="Latin",
                                 choices=(
                                     ("Latin", "Latin"),
                                     ("Syro Malabar", "Syro Malabar"),
                                     ("Syro Malankara", "Syro Malankara"),
                                     ("Other", "Other"),
                                     ("No Preference", "No Preference"),
                                 ), null=True, blank=True, )
    family_values = models.CharField(max_length=30, verbose_name="Family Values / Background", default="Traditional",
                                     choices=(
                                         ("Traditional", "Traditional"),
                                         ("Moderate", "Moderate"),
                                         ("Liberal", "Liberal"),
                                         ("No Preference", "No Preference"),
                                     ), null=True, blank=True, )
    # images
    passport_photo = CloudinaryField('passport_photo', null=True, blank=True)
    family_photo = CloudinaryField('family_photo', null=True, blank=True)
    your_photo_1 = CloudinaryField('your_photo_1', null=True, blank=True)
    your_photo_2 = CloudinaryField('your_photo_2', null=True, blank=True)
    your_photo_3 = CloudinaryField('your_photo_3', null=True, blank=True)

    passport_photo_1 = models.ImageField(upload_to=get_photo_path, null=True, blank=True)
    family_photo_1 = models.ImageField(upload_to=get_photo_path, null=True, blank=True)
    your_photo_1_1 = models.ImageField(upload_to=get_photo_path, null=True, blank=True)
    your_photo_2_1 = models.ImageField(upload_to=get_photo_path, null=True, blank=True)
    your_photo_3_1 = models.ImageField(upload_to=get_photo_path, null=True, blank=True)

    def get_cloudinary_photo_urls(self):
        return [
            self.passport_photo.url if self.passport_photo else None,
            self.family_photo.url if self.family_photo else None,
            self.your_photo_1.url if self.your_photo_1 else None,
            self.your_photo_2.url if self.your_photo_2 else None,
            self.your_photo_3.url if self.your_photo_3 else None,
        ]

    def image_handler(self, url: str, index: int):
        response = requests.get(url, stream=True)
        if response.status_code != requests.codes.ok:
            pass

        fp = BytesIO()
        fp.write(response.content)
        filename = url.split('/')[-1]
        if index == 0:
            self.passport_photo_1.save(filename, files.File(fp))
        elif index == 1:
            self.family_photo_1.save(filename, files.File(fp))
        elif index == 2:
            self.your_photo_1_1.save(filename, files.File(fp))
        elif index == 3:
            self.your_photo_2_1.save(filename, files.File(fp))
        elif index == 4:
            self.your_photo_3_1.save(filename, files.File(fp))
        else:
            raise ValueError("Value not supported, usage range [0, 4]\n")

    def save(self, urls=None, *args, **kwargs):
        print(urls)
        if urls:
            for i, url in enumerate(urls, 0):
                if not url:
                    continue
                else:
                    self.image_handler(url, i)
        super(MatrimonyApplication, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Receipt(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    user_application = models.ForeignKey(MatrimonyApplication, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=100, default='', blank=True, null=True)
    payment_id = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.modified)


class MeetAndGreetRequest(models.Model):
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_by')
    other_party = models.ForeignKey(User, on_delete=models.CASCADE, related_name='other_party')
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    meet_date = models.DateField(default=timezone.now)
    meet_slot = models.CharField(max_length=10, default='10-11', choices=(
        ('10-11', '10-11am'),
        ('11-12', '11-12pm'),
        ('14-15', '2-3pm'),
        ('15-16', '3-4am'),
        ('16-17', '4-5am'),
    ))

    def __str__(self):
        return f"From: {self.meet_slot} on: {self.meet_date}"
