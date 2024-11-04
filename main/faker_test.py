from .models import MatrimonyApplication
from faker import Faker

import random
import functools
import numpy as np

nos = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "9"]


def get_random_phno():
    f = Faker('en_IN')
    np.random.shuffle(nos)
    phone_no = functools.reduce(lambda a, b: str(a) + str(b), nos)
    return phone_no


lang_list = ['English', 'Assamese', 'Bengali', 'Gujarati', 'Hindi', 'Kannada', 'Kashmiri', 'Konkani', 'Malayalam',
             'Manipuri', 'Marathi', 'Nepali', 'Oriya', 'Punjabi', 'Sanskrit', 'Sindhi', 'Tamil', 'Telugu', 'Urdu',
             'Bodo', 'Santhali', 'Maithili', 'Dogri']

lang_list.sort()

'''
Engineer
Chartered Accountant
Consultant
Physician
Lawyer
Aviator
Software Developer
Scientist
Secretary
Psychologist
Civil servant
Merchant
Veterinarian
Professor
Makeup Artist
Model
Financial Analyst
Architect
Civil engineer
Domestic worker
Politician
Army officer
Financial adviser
Comedian
Author
Sailor
Chef
Mechanical engineer
Graphic Designer
Recruiter
Furniture Designer
Sales management
Fashion Designer
Surveyor
Emergency medical technician
Design Engineer
Computer operator
Drafter
Technical writer
Analyst
Political scientist
Flight engineer
Historian
Firefighter
Loan Officer
Hawker
Magistrate
Stock broker
'''

'''
Engineer
Chartered Accountant
Physician
Consultant
Lawyer
Aviator
Scientist
Secretary
Software Developer
Psychologist
Veterinarian
Merchant
Civil servant
Makeup Artist
Model
Financial Analyst
Professor
Architect
Domestic worker
Civil engineer
Army officer
Politician
Comedian
Financial adviser
Sailor
Author
Mechanical engineer
Sales management
Graphic Designer
Surveyor
Drafter
Design Engineer
Emergency medical technician
Furniture Designer
Computer operator
Recruiter
Chef
Political scientist
Fashion Designer
Flight engineer
Technical writer
Historian
Firefighter
Loan Officer
Hawker
Magistrate
Stock broker
Microbiologist
Doctor
Surgeon
'''


def createApplication(f):
    app = MatrimonyApplication.objects.create()
    app.first_name = f.first_name_female()
    app.last_name = f.last_name_female()
    app.language = random.choice(lang_list)
    app.gender = "Female"
    app.phone_number = "+91" + get_random_phno()
    app.email = f.email()
    app.city = f.city()
    app.state = "Karnataka"
    app.addr_1 = f.address()
    app.country = "India"
    app.pin_code = "700123"

    app.annual_income = float(random.randrange(10000, 5000000, 10000))

    app.education_level = random.choice(["Less Than 10th", '10th', '12th', 'Graduate', 'Post Graduate', 'Other'])

    app.height = float(random.randrange(120, 180, 1))
    app.weight = float(random.randrange(40, 80, 1))
    app.date_of_birth = f.date()
    app.place_of_birth = f.city()
    app.occupation = f.job()

    app.marital_status = random.choice(["Divorced", "Single", "Widowed"])
    app.former_spouse_name_1 = f.name_male()
    app.marriage_date_1 = f.date()
    app.divorced = f.date()
    app.marriage_annulment_date = f.date()

    app.fathers_name = f.name_male()
    app.mothers_name = f.name_female()

    app.salary_lower = float(random.randrange(0, 50000, 10000))
    app.salary_upper = float(random.randrange(60000, 5000000, 10000))

    app.lower_age = random.randrange(20, 30, 1)
    app.upper_age = random.randrange(30, 60, 1)

    app.education = "Less Than 10th"

    app.employment = f.job()

    app.save()