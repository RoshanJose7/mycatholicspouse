from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from email.mime.image import MIMEImage

professions = [
    "Psychologist", "Epidermiologist", "General Physician", "Dentist", "Pediatrician",
    "Radiologist", "Urologist", "Oncologist", "Gynaecologist", "Surgeon", "Neurosurgeon",
    "ENT Specialist", "Psychiatrist", "Orthopedist", "Optometrist", "Nurse",

    "Comedian", "Actor", "Director", "Producer", "Singer", "Musician", "Youtuber", "Writer", "Dancer", "Stuntman",
    "On-Site Technician",

    "Computer Scientist", "IT Professional", "Biologist", "Neuroscientist", "Zoologist", "Botanist", "Geographer",
    "Chemist", "Historian",
    "Archaeologist", "Microbiologist", "Economist", "Statistician", "Data Scientist", "Pathologist", "Paleontologist",
    "Political Scientist", "Herpetologist",

    "Civil Engineer", "Mechanical Engineer", "Electronics & (Tele)communications Engineer", "Electical Engineer",
    "Chemical Engineer", "Software Engineer", "AI Engineer", "Aeronautical Engineer", "Mechatronics Engineer",

    "Primary School Teacher", "Higher Secondary Teacher", "Lecturer", "Professor", "Kindergarten Teacher",
    "Tuition Teacher",

    "Banker", "Chatered Accountant", "Chef", "Product Manager", "Sales Executive", "Finance Manager", "Bank Manager",
    "Sales Manager", "Accountant", "Budget Analyst",
    "Investment Analyst", "Business Consultant", "Management Consultant", "Treasurer and Finance Officer",

    "Lawyer", "Railways Officer", "Government Officer", "Railways Staff", "Law Enforcement Officer",
    "Ticket Controller", "Train Dispatcher", "Signalman", "Brakeman", "Station Manager",
    "Deputy / Assistant Station Manager", "Train Driver"

                                          "Tailor", "Barber", "Mechanic", "Shopkeeper", "Bus Triver", "Taxi Driver",
]


class Connector():

    def __init__(self, user_app):
        self.user = user_app.user
        self.connect, created = Connection.objects.get_or_create(
            user=user_app.email)
        self.connect.save()

    def mail_send(self, event):
        subject = f"[{event['subject']}] New Notification!"
        html_content = get_template(
            'main/connector_event_template.html').render({'event': event}
                                                         )
        mail = EmailMultiAlternatives(
            subject, html_content, from_email="welcome@marryacatholic.com", to=[event["receiver"]],
            bcc=["marryacatholic@gmail.com"])
        mail.mixed_subtype = 'related'
        mail.attach_alternative(html_content, "text/html")
        img_dir = 'static'
        image = 'marry_a_catholic_favicon.png'
        file_path = settings.BASE_DIR / 'static/main/img/marry_a_catholic_favicon.png'
        with open(file_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        mail.attach(img)
        mail.send()

    def has_liked(self, liked_app):
        events = []
        temp_connect, _created = Connection.objects.get_or_create(
            user=liked_app.email)
        temp_user = liked_app.user

        send_mail_bool = temp_user in self.connect.has_liked.all()

        if temp_user in self.connect.was_blocked.all():
            return

        # ! Other User's Update
        if self.user in temp_connect.has_liked.all():
            event = {}
            temp_connect.has_liked.remove(self.user)
            temp_connect.matched.add(self.user)
            event["type"] = "Matched"
            event["subject"] = "It's a Match"
            event["message"] = "You have matched with "
            event["user"] = f"{self.user.first_name}  {self.user.last_name}."
            event["url"] = f"https://marryacatholic.com/user-view/{self.user.matrimonyapplication.id}/"
            event["receiver"] = temp_user.email
            events.append(event)
        else:
            event = {}
            temp_connect.was_liked.add(self.user)
            event["type"] = "Liked"
            event["subject"] = "New Like"
            event["message"] = "You were liked by "
            event["user"] = f"{self.user.first_name[0]}  {self.user.last_name[0]}."
            event["receiver"] = temp_user.email
            event["url"] = f"https://marryacatholic.com/user-view/{self.user.matrimonyapplication.id}/"
            events.append(event)

        # ! This User's Update
        if temp_user in self.connect.was_liked.all():
            event = {}
            self.connect.was_liked.remove(temp_user)
            self.connect.matched.add(temp_user)
            event["type"] = "Matched"
            event["subject"] = "It's a Match"
            event["message"] = "You have matched with "
            event["user"] = f"{temp_user.first_name}  {temp_user.last_name}"
            event["receiver"] = self.user.email
            event["url"] = f"https://marryacatholic.com/user-view/{temp_user.matrimonyapplication.id}/"
            events.append(event)
        else:
            self.connect.has_liked.add(temp_user)

        temp_connect.save()
        self.connect.save()

        for i in range(len(events)):
            self.mail_send(events[i])
        # * self.user.save()
        # * temp_user.save()

    def has_disliked(self, disliked_app):
        temp_connect, _created = Connection.objects.get_or_create(
            user=disliked_app.email)
        temp_user = disliked_app.user

        # ! Other User's Update
        if self.user in temp_connect.was_liked.all():
            temp_connect.was_liked.remove(self.user)
        elif self.user in temp_connect.matched.all():
            temp_connect.matched.remove(self.user)
            temp_connect.has_liked.add(self.user)

        # ! This User's Update
        if temp_user in self.connect.has_liked.all():
            self.connect.has_liked.remove(temp_user)
        elif temp_user in self.connect.matched.all():
            self.connect.matched.remove(temp_user)
            self.connect.was_liked.add(temp_user)

        # TODO Em@il Part

        temp_connect.save()
        self.connect.save()

    def has_unliked(self, unliked_app):
        temp_connect, _created = Connection.objects.get_or_create(
            user=unliked_app.email)
        temp_user = unliked_app.user
        if temp_user in self.connect.has_unliked.all():
            self.connect.has_unliked.remove(temp_user)
            temp_connect.was_unliked.remove(self.user)
        else:
            if temp_user in self.connect.has_liked.all():
                self.connect.has_liked.remove(temp_user)
                temp_connect.was_liked.remove(self.user)
            elif self.user in temp_connect.matched.all():
                temp_connect.matched.remove(self.user)
                self.connect.matched.remove(temp_user)
                temp_connect.has_liked.add(self.user)

            self.connect.has_unliked.add(temp_user)
            temp_connect.was_unliked.add(self.user)  # just backend

        self.connect.save()
        temp_connect.save()

    def has_blocked(self, blocked_app):
        temp_connect, _created = Connection.objects.get_or_create(
            user=blocked_app.email)
        temp_user = blocked_app.user

        if temp_user in self.connect.has_blocked.all():
            self.connect.has_blocked.remove(temp_user)
            temp_connect.was_blocked.remove(self.user)
        else:
            if temp_user in self.connect.has_liked.all():
                temp_connect.was_liked.remove(self.user)
                self.connect.has_liked.remove(temp_user)
            elif self.user in temp_connect.matched.all():
                temp_connect.matched.remove(self.user)
                self.connect.matched.remove(temp_user)
            elif temp_user in self.connect.has_unliked.all():
                self.connect.has_unliked.remove(temp_user)
                temp_connect.was_unliked.remove(self.user)

            self.connect.has_blocked.add(temp_user)
            temp_connect.was_blocked.add(self.user)

        self.connect.save()
        temp_connect.save()


class MatchMaker():
    def __init__(self):
        self.set_q = None
        self.set_not_q = None
        self.set_final = None
        self.all_apps = None

    def make_match(self, user_application: MatrimonyApplication):
        conn, _ = Connection.objects.get_or_create(
            user=user_application.user.email)
        all_applications = MatrimonyApplication.objects.filter(
            gender='Female' if user_application.gender == "Male" else "Male", is_approved=True, status='Active') \
            .exclude(
            user__in=conn.matched.all()) \
            .exclude(user__in=conn.has_liked.all()) \
            .exclude(user__in=conn.has_unliked.all()) \
            .exclude(user__in=conn.has_blocked.all()) \
            .exclude(user__in=conn.was_blocked.all())

        np = 'No Preference'

        prefer_disable = user_application.special_needs
        prefer_community = user_application.community
        prefer_language = user_application.language.split(',') if user_application.language is not None else []
        prefer_widowed = user_application.widowed
        prefer_lower_age = user_application.lower_age
        prefer_upper_age = user_application.upper_age
        prefer_lower_salary = user_application.salary_lower
        prefer_upper_salary = user_application.salary_upper
        prefer_occupation = user_application.employment

        q = all_applications

        if prefer_disable != np:
            q = q.filter(disability=prefer_disable)

        if prefer_community != np:
            q = q.filter(rite=prefer_community)

        if prefer_language[0] != np:
            q = q.filter(mother_tongue__in=prefer_language)

        if prefer_widowed != np:
            q = q.filter(marital_status__in=[
                'Single', 'Divorced'] if prefer_widowed == "No" else ["Widowed"])

        if prefer_lower_age:
            q = q.filter(age__gte=prefer_lower_age)

        if prefer_upper_age:
            q = q.filter(age__lte=prefer_upper_age)

        if prefer_lower_salary:
            q = q.filter(annual_income__gte=prefer_lower_salary)

        if prefer_upper_salary:
            q = q.filter(annual_income__lte=prefer_upper_salary)

        set_all_apps = set(all_applications)
        self.all_apps = all_applications
        set_q = set(q)
        set_not_q = list(set_all_apps - set_q)
        set_final = list(set_q) + list(set_not_q)
        self.set_q = list(set_q)
        self.set_not_q = set_not_q
        self.set_final = set_final

    def get_results_from_homepage(self, user_application: MatrimonyApplication, post_data):
        conn, _ = Connection.objects.get_or_create(
            user=user_application.user.email)
        all_applications = MatrimonyApplication.objects.filter(
            gender=post_data.get("gender") if post_data.get(
                "gender") != "Any" else "Male" if user_application.gender == "Female" else "Male", is_approved=True,
            status='Active').exclude(
            user__in=conn.matched.all()) \
            .exclude(user__in=conn.has_liked.all()) \
            .exclude(user__in=conn.has_unliked.all()) \
            .exclude(user__in=conn.has_blocked.all()) \
            .exclude(user__in=conn.was_blocked.all())

        np = 'No Preference'
        prefer_community = np if post_data.get("rite") == "Any" else post_data.get("rite")
        if post_data.get("age") == "Any":
            prefer_lower_age, prefer_upper_age = 0, 0
        else:
            prefer_lower_age, prefer_upper_age = list(map(int, post_data.get("age").split('-')))
        q = all_applications
        if prefer_community != np:
            q = q.filter(rite=prefer_community)
        if prefer_lower_age:
            q = q.filter(age__gte=prefer_lower_age)
        if prefer_upper_age:
            q = q.filter(age__lte=prefer_upper_age)

        set_all_apps = set(all_applications)
        self.all_apps = all_applications
        set_q = set(q)
        set_not_q = list(set_all_apps - set_q)
        set_final = list(set_q) + list(set_not_q)
        self.set_q = list(set_q)
        self.set_not_q = set_not_q
        self.set_final = set_final

    def get_results(self, user_application: MatrimonyApplication, post_data):
        conn, _ = Connection.objects.get_or_create(
            user=user_application.user.email)
        all_applications = MatrimonyApplication.objects.filter(
            gender='Female' if user_application.gender == "Male" else "Male", is_approved=True,
            status='Active').exclude(
            user__in=conn.matched.all()).exclude(user__in=conn.has_liked.all()) \
            .exclude(user__in=conn.has_liked.all()) \
            .exclude(user__in=conn.has_unliked.all()) \
            .exclude(user__in=conn.has_blocked.all()) \
            .exclude(user__in=conn.was_blocked.all())

        np = 'No Preference'

        # prefer_disable = user_application.special_needs
        prefer_community = list(filter(lambda x: x != "No Preference", post_data.getlist(
            'rite'))) if len(post_data.getlist('rite')) > 1 else [post_data.getlist('rite')[0]]
        prefer_language = list(filter(lambda x: x != "No Preference", post_data.getlist('mother_tongue'))) if len(
            post_data.getlist('mother_tongue')) > 1 else [post_data.getlist('mother_tongue')[0]]
        # prefer_widowed = user_application.widowed
        prefer_lower_age = int(post_data.get("lower-age"))
        prefer_upper_age = int(post_data.get("upper-age"))
        prefer_lower_salary = float(post_data.get("lower-salary"))
        prefer_upper_salary = float(post_data.get("upper-salary"))

        l = [prefer_community, prefer_language, prefer_lower_age,
             prefer_upper_age, prefer_lower_salary, prefer_upper_salary]
        print(l)
        print(list(map(type, l)))
        # prefer_occupation = user_application.employment

        q = all_applications

        # if prefer_disable != np:
        #     q = q.filter(disability = prefer_disable)

        if prefer_community[0] != np:
            q = q.filter(rite__in=prefer_community)

        if prefer_language[0] != np:
            q = q.filter(mother_tongue__in=prefer_language)

        # if prefer_widowed != np:
        #     q = q.filter(marital_status__in = ['Single', 'Divorced'] if prefer_widowed == "No" else ["Widowed"])

        if prefer_lower_age:
            q = q.filter(age__gte=prefer_lower_age)

        if prefer_upper_age:
            q = q.filter(age__lte=prefer_upper_age)

        if prefer_lower_salary:
            q = q.filter(annual_income__gte=prefer_lower_salary)

        if prefer_upper_salary:
            q = q.filter(annual_income__lte=prefer_upper_salary)

        set_all_apps = set(all_applications)
        self.all_apps = all_applications
        set_q = set(q)
        set_not_q = list(set_all_apps - set_q)
        set_final = list(set_q) + list(set_not_q)
        self.set_q = list(set_q)
        self.set_not_q = set_not_q
        self.set_final = set_final


'''
from main.matchmaking import MatchMaker
from main.models import MatrimonyApplication
x = MatrimonyApplication.objects.get(id = 15)
'''
