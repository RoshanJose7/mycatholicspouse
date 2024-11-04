from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

import csv
import json
import razorpay
from datetime import date
from email.mime.image import MIMEImage

from .forms import *
from .models import Receipt
from .matchmaking import Connector, MatchMaker

# Razorpay Docs
client = razorpay.Client(auth=(settings.RZPAY_KEY, settings.RZPAY_SECRET))

m = MatchMaker()


def form_submit(request):
    # try:
    print(request.POST, request.FILES)
    print(','.join(list(filter(lambda x: x != "No Preference", request.POST.getlist('language'))) if len(
        request.POST.getlist('language')) > 1 else [request.POST.getlist('language')[0]]))
    post = {k: v for k, v in request.POST.items()}
    del post['csrfmiddlewaretoken']
    form = MatrimonyApplicationForm(request.POST, request.FILES)
    if form.is_valid():
        print("valid")
        application = form.save(commit=False)
        application.mother_tongue = request.POST.get("mother_tongue")
        application.gender = request.POST.get("Gender")
        application.phone_number = "+91" + request.POST.get("phone_number")
        if len(MatrimonyApplication.objects.filter(phone_number=application.phone_number)):
            return HttpResponse(
                "<script>alert('Phone number already exists in our database. If you yourself filled the form before, please check for a mail from welcome@marryacatholic.com, do check the spam section if not in inbox. If you think that this is an error, contact site admin.'); window.history.back();</script>")
        application.education_level = request.POST.get("Education Level")
        print(application.education_level,
              request.POST.get("Education Level"))
        application.date_of_birth = timezone.datetime(
            *list(map(int, request.POST.get("date_of_birth").split('-'))))
        application.age = round(
            (date.today() - application.date_of_birth.date()).days / 365.2425)
        application.rite = request.POST.get("rite")
        application.diet = request.POST.get("diet")
        application.smoke = request.POST.get("smoke")
        application.drink = request.POST.get("drink")
        application.health_issues = request.POST.get("health_issues")
        application.marital_status = request.POST.get("Marital Status")
        application.disability = request.POST.get("Disability")
        try:
            if application.marital_status == "Divorced":
                application.marriage_date_1 = timezone.datetime(
                    *list(map(int, request.POST.get("marriage_date_1").split('-'))))
                application.divorce_date = timezone.datetime(
                    *list(map(int, request.POST.get("divorce_date").split('-'))))
                application.marriage_annulment_date = timezone.datetime(
                    *list(map(int, request.POST.get("marriage_annulment_date").split('-'))))
            elif application.marital_status == "Widowed":
                application.marriage_date_2 = timezone.datetime(
                    *list(map(int, request.POST.get("marriage_date_2").split('-'))))
                application.date_of_death = timezone.datetime(
                    *list(map(int, request.POST.get("date_of_death").split('-'))))
        except ValueError:
            pass
        application.values = request.POST.get("Family Values")
        application.special_needs = request.POST.get("special_needs")
        application.widowed = request.POST.get("Widow / Widower")
        application.language = ','.join(list(filter(lambda x: x != "No Preference", request.POST.getlist(
            'language'))) if len(request.POST.getlist('language')) > 1 else [request.POST.getlist('language')[0]])
        application.community = request.POST.get("community")
        application.family_values = request.POST.get(
            "Family Background / Values")
        application.migrated = False
        application.save()

        subject = "New Registration"
        html_content = get_template(
            'main/email_test.html').render({'data': post, 'app': application})
        mail = EmailMessage(
            subject,
            html_content,
            from_email="welcome@marryacatholic.com",
            to=["fwcbangalore@gmail.com", ]

        )
        mail.content_subtype = "html"
        for k, v in request.FILES.items():
            mail.attach(
                f'{k}.{v.name.split(".")[-1]}', v.read(), v.content_type)
        mail.send()

        subject = "Complete Registration"
        html_content = get_template(
            'main/payment_email.html').render({'app': application})
        mail = EmailMultiAlternatives(
            subject, html_content, from_email="welcome@marryacatholic.com", to=[application.email, ],
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
        try:
            mail.send()
        except:
            pass
        return redirect('select-plan', application.id)
    else:
        errors = ' \\n'.join(list(map(
            lambda x, y: f"{x}: {' '.join(list(map(lambda a: str(*a), y)))}", form.errors.as_data().keys(),
            form.errors.as_data().values())))
        time = str(timezone.now())
        subject = f"Registration Attempt [ERROR ID : {time}]"
        post['error_id'] = time
        post['error'] = errors
        html_content = get_template(
            'main/email_test.html').render({'data': post})
        mail = EmailMessage(subject, html_content, from_email="welcome@marryacatholic.com",
                            to=[
                                "marryacatholic@gmail.com"
                            ]

                            )
        mail.content_subtype = "html"
        for k, v in request.FILES.items():
            mail.attach(
                f'{k}.{v.name.split(".")[-1]}', v.read(), v.content_type)
        mail.send()
        return HttpResponse(
            f"<script>alert('Error ID: {time}.\\n {errors} \\n If you yourself filled the form before, please check for a mail from welcome@marryacatholic.com, do check the spam section if not in inbox. If you think that this is an error, send a mail to the site admin: fwcbangalore@gmail.com with screenshots of the error (most importantly, the Error ID).'); window.history.back();</script>")


# except OperationalError as e:
#     return HttpResponse("<script>alert('" + str(e) + "'); window.history.back();</script>")
# except:
#     return HttpResponse("<script>alert('There was a technical issue. Please try filling the form again later. If the issue persists, contact site admin.'); window.history.back();</script>")


def approving_user(email):
    appl = MatrimonyApplication.objects.filter(email=email)[0]
    new_user, _ = User.objects.get_or_create(email=email)
    password = User.objects.make_random_password()
    new_user.set_password(password)
    new_user.username = email
    new_user.first_name = appl.first_name
    # new_user.middle_name = appl.middle_name
    new_user.last_name = appl.last_name
    appl.user = new_user
    appl.is_approved = True
    subject = "[Approval] You've been approved!"
    html_content = get_template(
        'main/mail_approval.html').render({'username': new_user.username, 'password': password})
    # mail = EmailMessage(subject, html_content, from_email = "welcome@marryacatholic.com", to = [ new_user.email ], headers={})
    # mail.content_subtype = "html"
    mail = EmailMultiAlternatives(
        subject, html_content, from_email="welcome@marryacatholic.com",
        to=[new_user.email,
            ], bcc=["marryacatholic@gmail.com"])
    mail.mixed_subtype = 'related'
    mail.attach_alternative(html_content, "text/html")
    img_dir = 'static'
    image = 'marry_a_catholic_favicon.png'
    # file_path = os.path.join(img_dir, image)
    file_path = settings.BASE_DIR / 'static/main/img/marry_a_catholic_favicon.png'
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    mail.attach(img)
    appl.status = 'Active'
    appl.save()
    new_user.save()
    mail.send()
    return password


def updating_user(email):
    appl = MatrimonyApplication.objects.filter(email=email)[0]
    new_user, _ = User.objects.get_or_create(email=email)
    password = User.objects.make_random_password()
    new_user.set_password(password)
    new_user.username = email
    new_user.first_name = appl.first_name
    # new_user.middle_name = appl.middle_name
    new_user.last_name = appl.last_name
    appl.user = new_user
    appl.is_approved = True
    subject = "[Notification] You've successfully updated your info!"
    html_content = get_template(
        'main/updated_user.html').render({'username': new_user.username, 'password': password})
    # mail = EmailMessage(subject, html_content, from_email = "welcome@marryacatholic.com", to = [ new_user.email ], headers={})
    # mail.content_subtype = "html"
    mail = EmailMultiAlternatives(
        subject, html_content, from_email="welcome@marryacatholic.com", to=['marryacatholic@gmail.com', new_user.email])
    mail.mixed_subtype = 'related'
    mail.attach_alternative(html_content, "text/html")
    img_dir = 'static'
    image = 'marry_a_catholic_favicon.png'
    # file_path = os.path.join(img_dir, image)
    file_path = settings.BASE_DIR / 'static/main/img/marry_a_catholic_favicon.png'
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    mail.attach(img)
    appl.save()
    new_user.save()
    # mail.send()
    return password


@csrf_exempt
def approve_user(request, email):
    try:
        password = approving_user(email)
        return JsonResponse({"code": "200", "password": password})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def batch_approval(request):
    try:
        batch_emails = json.loads(request.body)['emails']
        passwords_dict = {}
        for email in batch_emails:
            passwords_dict[email] = approving_user(email)
        print(passwords_dict)
        subject = "Batch Approval was successful!"
        html_content = get_template(
            'main/mail_batch_approval.html').render({'passwords_dict': passwords_dict})
        mail = EmailMultiAlternatives(subject, html_content, from_email="welcome@marryacatholic.com", to=[
            "fwcbangalore@gmail.com"])
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
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def edit_profile(request, email):
    instance = MatrimonyApplication.objects.filter(email=email)[0]
    if request.method == "POST":
        # deletion_dict = {
        #     'passport_photo': instance.passport_photo.public_id if instance.passport_photo is not None else None,
        #     'family_photo': instance.family_photo.public_id if instance.family_photo is not None else None,
        #     'your_photo_1': instance.your_photo_1.public_id if instance.your_photo_1 is not None else None,
        #     'your_photo_2': instance.your_photo_2.public_id if instance.your_photo_2 is not None else None,
        #     'your_photo_3': instance.your_photo_3.public_id if instance.your_photo_3 is not None else None,
        # }
        form = MatrimonyApplicationEditForm(
            request.POST, request.FILES, instance=instance)
        print(request.FILES)
        if form.is_valid():
            # for i in deletion_dict.keys():
            #     if i in form.changed_data:
            #         if deletion_dict[i] is not None:
            #             status = cloudinary.uploader.destroy(deletion_dict[i], invalidate=True)
            app = form.save(commit=False)
            app.gender = request.POST.get("Gender")
            app.mother_tongue = request.POST.get("mother_tongue")
            app.phone_number = "+91" + request.POST.get("phone_number")
            app.education_level = request.POST.get("Education Level")
            print(app.education_level, request.POST.get("Education Level"))
            app.date_of_birth = timezone.datetime(
                *list(map(int, request.POST.get("date_of_birth").split('-'))))
            app.rite = request.POST.get("rite")
            app.diet = request.POST.get("diet")
            app.smoke = request.POST.get("smoke")
            app.drink = request.POST.get("drink")
            app.health_issues = request.POST.get("health_issues")
            app.marital_status = request.POST.get("Marital Status")
            app.disability = request.POST.get("Disability")
            try:
                if app.marital_status == "Divorced":
                    app.marriage_date_1 = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_date_1").split('-'))))
                    app.divorce_date = timezone.datetime(
                        *list(map(int, request.POST.get("divorce_date").split('-'))))
                    app.marriage_annulment_date = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_annulment_date").split('-'))))
                elif app.marital_status == "Widowed":
                    app.marriage_date_2 = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_date_2").split('-'))))
                    app.date_of_death = timezone.datetime(
                        *list(map(int, request.POST.get("date_of_death").split('-'))))
            except ValueError:
                pass
            app.values = request.POST.get("Family Values")
            app.special_needs = request.POST.get("special_needs")
            app.widowed = request.POST.get("Widow / Widower")
            app.community = request.POST.get("community")
            app.language = ','.join(list(filter(lambda x: x != "No Preference", request.POST.getlist(
                'language'))) if len(request.POST.getlist('language')) > 1 else [request.POST.getlist('language')[0]])
            app.family_values = request.POST.get("Family Background / Values")
            print(app.education_level)
            print(app.weight)
            app.save()
    return redirect('profile', email=email)


@csrf_exempt
def admin_edit_profile(request, email):
    instance = MatrimonyApplication.objects.filter(email=email)[0]
    if request.method == "POST":
        # deletion_dict = {
        #     'passport_photo': instance.passport_photo.public_id if instance.passport_photo is not None else None,
        #     'family_photo': instance.family_photo.public_id if instance.family_photo is not None else None,
        #     'your_photo_1': instance.your_photo_1.public_id if instance.your_photo_1 is not None else None,
        #     'your_photo_2': instance.your_photo_2.public_id if instance.your_photo_2 is not None else None,
        #     'your_photo_3': instance.your_photo_3.public_id if instance.your_photo_3 is not None else None,
        # }
        form = MatrimonyApplicationEditForm(
            request.POST, request.FILES, instance=instance)
        print(request.FILES)
        if form.is_valid():
            # for i in deletion_dict.keys():
            #     if i in form.changed_data:
            #         if deletion_dict[i] is not None:
            #             status = cloudinary.uploader.destroy(deletion_dict[i], invalidate=True)
            app = form.save(commit=False)
            app.gender = request.POST.get("Gender")
            app.mother_tongue = request.POST.get("mother_tongue")
            app.phone_number = "+91" + request.POST.get("phone_number")
            app.education_level = request.POST.get("Education Level")
            print(app.education_level, request.POST.get("Education Level"))
            app.date_of_birth = timezone.datetime(
                *list(map(int, request.POST.get("date_of_birth").split('-'))))
            app.rite = request.POST.get("rite")
            app.diet = request.POST.get("diet")
            app.smoke = request.POST.get("smoke")
            app.drink = request.POST.get("drink")
            app.health_issues = request.POST.get("health_issues")
            app.marital_status = request.POST.get("Marital Status")
            app.disability = request.POST.get("Disability")
            try:
                if app.marital_status == "Divorced":
                    app.marriage_date_1 = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_date_1").split('-'))))
                    app.divorce_date = timezone.datetime(
                        *list(map(int, request.POST.get("divorce_date").split('-'))))
                    app.marriage_annulment_date = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_annulment_date").split('-'))))
                elif app.marital_status == "Widowed":
                    app.marriage_date_2 = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_date_2").split('-'))))
                    app.date_of_death = timezone.datetime(
                        *list(map(int, request.POST.get("date_of_death").split('-'))))
            except ValueError:
                pass
            app.values = request.POST.get("Family Values")
            app.special_needs = request.POST.get("special_needs")
            app.widowed = request.POST.get("Widow / Widower")
            app.community = request.POST.get("community")
            app.language = ','.join(list(filter(lambda x: x != "No Preference", request.POST.getlist(
                'language'))) if len(request.POST.getlist('language')) > 1 else [request.POST.getlist('language')[0]])
            app.family_values = request.POST.get("Family Background / Values")
            print(app.education_level)
            print(app.weight)
            app.save()
    return redirect('admin-application-details', email)


@csrf_exempt
def update_profile_id(request, id):
    instance = MatrimonyApplication.objects.get(id=id)
    if request.method == "POST":
        form = MatrimonyApplicationEditForm(
            request.POST, request.FILES, instance=instance)
        if form.is_valid():
            app = form.save(commit=False)
            app.gender = request.POST.get("Gender")
            app.mother_tongue = request.POST.get("mother_tongue")
            app.phone_number = "+91" + request.POST.get("phone_number")
            app.education_level = request.POST.get("Education Level")
            print(app.education_level, request.POST.get("Education Level"))
            app.date_of_birth = timezone.datetime(
                *list(map(int, request.POST.get("date_of_birth").split('-'))))
            app.rite = request.POST.get("rite")
            app.diet = request.POST.get("diet")
            app.smoke = request.POST.get("smoke")
            app.drink = request.POST.get("drink")
            app.health_issues = request.POST.get("health_issues")
            app.marital_status = request.POST.get("Marital Status")
            app.disability = request.POST.get("Disability")
            try:
                if app.marital_status == "Divorced":
                    app.marriage_date_1 = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_date_1").split('-'))))
                    app.divorce_date = timezone.datetime(
                        *list(map(int, request.POST.get("divorce_date").split('-'))))
                    app.marriage_annulment_date = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_annulment_date").split('-'))))
                elif app.marital_status == "Widowed":
                    app.marriage_date_2 = timezone.datetime(
                        *list(map(int, request.POST.get("marriage_date_2").split('-'))))
                    app.date_of_death = timezone.datetime(
                        *list(map(int, request.POST.get("date_of_death").split('-'))))
            except ValueError:
                pass
            app.values = request.POST.get("Family Values")
            app.special_needs = request.POST.get("special_needs")
            app.widowed = request.POST.get("Widow / Widower")
            app.community = request.POST.get("community")
            app.language = ','.join(list(filter(lambda x: x != "No Preference", request.POST.getlist(
                'language'))) if len(request.POST.getlist('language')) > 1 else [request.POST.getlist('language')[0]])
            app.family_values = request.POST.get("Family Background / Values")
            print(app.education_level)
            print(app.weight)

            app.save()

            _ = updating_user(app.email)
            return render(request, 'main/updated_message.html')
    return JsonResponse({'code': "200"})


@csrf_exempt
def rejection_admin(request):
    # print('Fucking Diabolical Mate')
    try:
        dic = json.loads(request.body)
        email = dic["email"]
        message = dic["message"]
        appl = MatrimonyApplication.objects.filter(email=email)[0]
        appl.is_rejected = True
        appl.status = 'Inactive'
        appl.save()
        latest_app_receipt = appl.receipt_set.filter(
            created__lte=appl.subs_end, paid=True)
        if len(latest_app_receipt) > 0:
            latest_app_receipt = latest_app_receipt.latest('modified')
            amount = float(latest_app_receipt.plan.price) * 100
            notes = {'msg': f'Refund for {latest_app_receipt.plan.plan_name}'}
            resp = client.payment.refund(
                latest_app_receipt.payment_id, int(amount))
            json.dump(resp, open('test.json', 'w'))
        subject = "[Rejection] Your application has been rejected!"
        html_content = get_template(
            'main/mail_rejection.html').render({'message': message})
        # mail = EmailMessage(subject, html_content, from_email = "welcome@marryacatholic.com", to = [ new_user.email ], headers={})
        # mail.content_subtype = "html"
        mail = EmailMultiAlternatives(
            subject, html_content, from_email="welcome@marryacatholic.com", to=[appl.email],
            bcc=["marryacatholic@gmail.com"])
        mail.mixed_subtype = 'related'
        mail.attach_alternative(html_content, "text/html")
        img_dir = 'static'
        image = 'marry_a_catholic_favicon.png'
        # file_path = os.path.join(img_dir, image)
        file_path = settings.BASE_DIR / 'static/main/img/marry_a_catholic_favicon.png'
        with open(file_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        mail.attach(img)
        mail.send()
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def liked(request, id):
    try:
        like_app = MatrimonyApplication.objects.get(id=id)
        c = Connector(request.user.matrimonyapplication)
        c.has_liked(like_app)
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def disliked(request, id):
    try:
        like_app = MatrimonyApplication.objects.get(id=id)
        c = Connector(request.user.matrimonyapplication)
        c.has_disliked(like_app)
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def unliked(request, id):
    try:
        like_app = MatrimonyApplication.objects.get(id=id)
        c = Connector(request.user.matrimonyapplication)
        c.has_unliked(like_app)
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def disunliked(request, id):
    try:
        like_app = MatrimonyApplication.objects.get(id=id)
        c = Connector(request.user.matrimonyapplication)
        c.has_unliked(like_app)
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def blocked(request, id):
    try:
        like_app = MatrimonyApplication.objects.get(id=id)
        c = Connector(request.user.matrimonyapplication)
        c.has_blocked(like_app)
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def disblocked(request, id):
    try:
        like_app = MatrimonyApplication.objects.get(id=id)
        c = Connector(request.user.matrimonyapplication)
        c.has_blocked(like_app)
        return JsonResponse({"code": "200"})
    except:
        return JsonResponse({"code": "404"})


@csrf_exempt
def check_cred(request, reg_id, password):
    try:
        f = MatrimonyApplication.objects.filter(reg_id=reg_id)[0]
        if f:
            if f.interim_password == password:
                return JsonResponse({"code": 200, "id": f.id})
        return JsonResponse({"code": 404})
    except:
        return JsonResponse({"code": 404})


@csrf_exempt
def order_generate(request, receipt_id):
    receipt: Receipt = Receipt.objects.get(id=receipt_id)
    notes = {'plan': f'{receipt.plan.plan_name}'}
    amount = 1.18 * float(receipt.plan.price)
    order_dict = {'amount': int(amount * 100), 'currency': "INR",
                  'receipt': str(receipt.id), 'notes': notes, 'payment_capture': '0'}
    order = client.order.create(order_dict)
    receipt.order_id = order['id']
    receipt.save()
    return JsonResponse({"code": 200, "order_id": order['id'], "amount": order_dict['amount']})


def switch_status(request, email, status):
    try:
        user = MatrimonyApplication.objects.get(email=email)
        user.status = status
        user.save()
        return JsonResponse({'code': 200})
    except:
        return JsonResponse({'code': 404})


@csrf_exempt
def check_status(request, email):
    try:
        user = MatrimonyApplication.objects.filter(email=email)
        if len(user) == 0:
            user = User.objects.filter(username=email)[0]
            if user.is_staff:
                return JsonResponse({'code': 200, 'response': True})
            else:
                return JsonResponse({'code': 200, 'response': False})
        else:
            user = user[0]
            # inactive users
            status = (
                (user.status != "Blocked" and user.is_approved and not user.is_rejected))
            return JsonResponse({'code': 200, 'response': status})
    except:
        return JsonResponse({'code': 404})


def send_mail_to_devs(start_or_stop: str, ids: str) -> None:
    message = f"Time : {timezone.now()} IDs: {ids}"
    mail = EmailMultiAlternatives(f'CRON Job {start_or_stop}', message, from_email="welcome@marryacatholic.com",
                                  to=["marryacatholic@gmail.com"])
    mail.send()


def php_call_api(request):
    # query users
    # filter(user -> (user.subs_end - timezone.now()).days < 5) | send_email() | return response

    users = MatrimonyApplication.objects.filter(subs_end__lte=timezone.now(
    ), status='Active', is_approved=True, is_paid=True, is_rejected=False)

    ids = ", ".join(list(map(lambda x: str(x.id), users)))
    send_mail_to_devs("Start", ids)

    for user in users:
        user.status = 'Inactive'
        user.save()
    subject = "[Expired] Your subscription plan has expired!"
    for user in users:
        days = (user.subs_end - timezone.now()).days
        message = f"Reminder: Your Plan has expired. Your profile won't be visible to other users. To resume the services, please renew your plan. You can renew your plan from your profile page, when your plan expires."
        html_content = get_template(
            'main/expiry.html').render({'message': message})
        mail = EmailMultiAlternatives(subject, html_content, from_email="welcome@marryacatholic.com", to=[
            user.email, ], bcc=["marryacatholic@gmail.com"])  # user.email
        mail.mixed_subtype = 'related'
        mail.attach_alternative(html_content, "text/html")
        img_dir = 'static'
        image = 'marry_a_catholic_favicon.png'
        # file_path = os.path.join(img_dir, image)
        file_path = settings.BASE_DIR / 'static/main/img/marry_a_catholic_favicon.png'
        with open(file_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        mail.attach(img)
        mail.send()

    users = MatrimonyApplication.objects.filter(subs_end__lte=timezone.now(
    ) + timezone.timedelta(days=3), status='Active', is_approved=True, is_paid=True, is_rejected=False)
    # send email to these users regarding expiry
    subject = "[Expiration] Your subscription plan is ending soon!"
    for user in users:
        days = (user.subs_end - timezone.now()).days
        message = f"Reminder: Your Plan will expire in {days} days. You can renew your plan from your profile page, when your plan expires."
        html_content = get_template(
            'main/expiry.html').render({'message': message})
        mail = EmailMultiAlternatives(subject, html_content, from_email="welcome@marryacatholic.com", to=[
            user.email, ])
        mail.mixed_subtype = 'related'
        mail.attach_alternative(html_content, "text/html")
        img_dir = 'static'
        image = 'marry_a_catholic_favicon.png'
        # file_path = os.path.join(img_dir, image)
        file_path = settings.BASE_DIR / 'static/main/img/marry_a_catholic_favicon.png'
        with open(file_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        mail.attach(img)
        mail.send()
    # send email to these users that their plan has expired
    ids = ", ".join(list(map(lambda x: str(x.id), users)))
    send_mail_to_devs("Stop", ids)
    return JsonResponse({'code': 304})


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def users2csv(request):
    if not request.user.is_staff:
        return HttpResponse('Not Authorized', status=403)
    users = MatrimonyApplication.objects.all()
    rows = []
    fields = MatrimonyApplication._meta.fields
    headers = []
    for field in fields:
        headers.append(field.name)
    rows.append(headers)
    pseudo_buffer = Echo()
    for user in users:
        row = []
        for field in headers:
            val = getattr(user, field)
            if callable(val):
                val = val()
            if type(val) == 'unicode':
                val = val.encode("utf-8")
            row.append(val)
        rows.append(row)
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv"
    )
    response['Content-Disposition'] = "attachment; filename='users_data.csv\'"
    return response

