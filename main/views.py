from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import login_required
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

import razorpay
import cloudinary
from uuid import uuid4
from email.mime.image import MIMEImage

from .faker_test import lang_list
from .forms import FilesForm, RadioForm, MatrimonyApplicationForm
from .models import MatrimonyApplication, PasswordResetToken, Receipt, Plan, MeetAndGreetRequest, Connection

# Razorpay Docs
client = razorpay.Client(auth=(settings.RZPAY_KEY, settings.RZPAY_SECRET))


def home(request):
    # photos = Photo.objects.all()
    boys = list(MatrimonyApplication.objects.filter(gender="Male", is_approved=True, status="Active"))[-2:]
    girls = list(MatrimonyApplication.objects.filter(gender="Female", is_approved=True, status="Active"))[-2:]
    return render(request, "main/home.html", {"boys": boys, "girls": girls})


@login_required
def admin_home(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    pending_applications = MatrimonyApplication.objects.filter(
        is_approved=False, is_paid=True, status="Active")
    context = {
        'normal_user': pending_applications,
    }
    return render(request, "main/admin_home.html", context)


@login_required
def admin_profile_preview(request, email):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    app = MatrimonyApplication.objects.filter(email=email)[0]
    li = app.language.split(",") if app.language is not None else []
    lang = {}
    for i in lang_list:
        if i in li:
            lang[i] = True
        else:
            lang[i] = False
    return render(request, "main/admin_profile_preview.html", context={'application': app, 'lang_list': lang})


@login_required
def print_profile_data(request, email):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    app = MatrimonyApplication.objects.filter(email=email)[0]
    li = app.language.split(",") if app.language is not None else []
    lang = {}
    for i in lang_list:
        if i in li:
            lang[i] = True
        else:
            lang[i] = False
    return render(request, "main/print_profile_data.html", context={'application': app, 'lang_list': lang})


def form_instruction(request):
    return render(request, 'main/form_fill_instruction.html')


def matrimony_form(request):
    if settings.MAINTENANCE:
        return render(request, 'main/maintain.html', {'lang_list': lang_list})
    return render(request, 'main/matrimony_form.html', {'lang_list': lang_list})


@csrf_exempt
def password_reset(request):
    if request.method == 'GET':
        return render(request, 'main/password_reset.html')
    else:
        email = request.POST.get("email")
        if len(User.objects.filter(email=email)) > 0:
            token, _ = PasswordResetToken.objects.get_or_create(email=email)
            token.token = uuid4()
            token.save()
            subject = "Password Reset"
            html_content = get_template(
                'main/password_reset_user.html').render({'HTTP_HOST': request.META['HTTP_HOST'], 'token': token})
            mail = EmailMultiAlternatives(
                subject, html_content, from_email="welcome@marryacatholic.com", to=[email, ],
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
                print("Some error has occurred. Please contact site admin.")
        return render(request, "main/password_reset.html")


@csrf_exempt
def password_reset_next(request, token):
    tokens = PasswordResetToken.objects.filter(token=token)
    if len(tokens) > 0:
        token: PasswordResetToken = tokens[0]
        if request.method == 'GET':
            return render(request, 'main/password_reset_next.html')
        else:
            password = request.POST.get('password1')
            user: User = User.objects.get(email=token.email)
            #            print(user)
            #            print(password)
            user.set_password(password)
            user.save()
            token.delete()
            return render(request, 'main/password_reset_next.html')
    else:
        return render(request, 'main/404.html')


def profile(request, email):
    user = User.objects.filter(email=email)[0]
    if request.user == user:
        app = MatrimonyApplication.objects.filter(user=user)[0]
        print(app)
        li = app.language.split(",") if app.language is not None else []
        lang = {}
        for i in lang_list:
            if i in li:
                lang[i] = True
            else:
                lang[i] = False
        return render(request, "main/profile.html",
                      {'app': app, 'lang_list': lang, 'expired': app.subs_end < timezone.now()})
    else:
        return render(request, "main/404.html")


def login_ID(request):
    return render(request, "main/reg_id_login.html")


def update_details(request, id):
    try:
        app = MatrimonyApplication.objects.get(id=id)
        li = app.language.split(",")
        lang = {}
        for i in lang_list:
            if i in li:
                lang[i] = True
            else:
                lang[i] = False
        return render(request, "main/update_details.html", {'app': app, 'lang_list': lang})
    except:
        return render(request, "main/404.html")


def tnc(request):
    return render(request, "main/tnc.html")


def priv_policy(request):
    return render(request, "main/priv_policy.html")


def dj_form(request):
    if request.method == 'POST':
        form = MatrimonyApplicationForm(request.POST, request.FILES)
        radform = RadioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MatrimonyApplicationForm()
        radform = RadioForm()
    return render(request, "main/dj_form.html", {'form': form, 'radForm': radform})


@csrf_exempt
def select_plan(request, app_id):
    try:
        app = MatrimonyApplication.objects.get(id=app_id)
        if request.method == 'GET':
            plans = Plan.objects.all()
            return render(request, 'main/select_plan.html', {'app_id': app_id, 'plans': plans})
        else:
            receipt: Receipt = Receipt.objects.create(user_application=app)
            plan: Plan = Plan.objects.get(id=request.POST.get("plans"))
            receipt.plan = plan
            receipt.save()
            return redirect('checkout', receipt.id)
    except:
        return render(request, 'main/404.html', {"message": "There seems to be a problem. Please contact site admin."})


@csrf_exempt
def checkout(request, receipt_id):
    receipt: Receipt = Receipt.objects.get(id=receipt_id)
    app = receipt.user_application
    plan = receipt.plan
    paid = receipt.paid
    if request.method == 'GET':
        return render(request, 'main/checkout.html',
                      {'receipt': receipt, 'plan': plan, 'app': app, 'paid': paid, "RZPAY_KEY": settings.RZPAY_KEY})
    else:
        receipt.paid = True
        app.plan = plan
        if timezone.now() < app.subs_end:
            app.subs_end = app.subs_end + timezone.timedelta(days=int(plan.duration))
        else:
            app.subs_start = timezone.now()
            app.subs_end = app.subs_start + timezone.timedelta(days=int(plan.duration))
        receipt.save()
        app.status = 'Active'
        app.is_rejected = False
        pay = client.order.payments(receipt.order_id)
        payments = pay['items']
        pay = \
        list(filter(lambda x: x['captured'] == False, sorted(payments, key=lambda x: x["created_at"], reverse=True)))[0]
        client.payment.capture(pay['id'], pay['amount'])
        receipt.payment_id = pay['id']
        receipt.save()
        if not app.is_paid:
            app.is_paid = True
            subject = "Payment Done"
            html_content = get_template(
                'main/new_mail_approval.html').render({'app': app})
            mail = EmailMultiAlternatives(
                subject, html_content, from_email="welcome@marryacatholic.com", to=["fwcbangalore@gmail.com", ],
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
                print("Some error has occurred. Please contact site admin.")
            # to the paying user
            subject = "[Registration] Payment Done Successfully"
            html_content = get_template(
                'main/mail_checkout.html').render({'app': app})
            mail = EmailMultiAlternatives(
                subject, html_content, from_email="welcome@marryacatholic.com", to=[app.email, ],
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
                print("Some error has occurred. Please contact site admin.")
        app.save()
        return render(request, 'main/checkout.html',
                      {'receipt': receipt, 'plan': plan, 'app': app, 'paid': receipt.paid,
                       "RZPAY_KEY": settings.RZPAY_KEY})


def about_us(request):
    return render(request, 'main/about_us.html')


def contact_us(request):
    return render(request, 'main/contact_us.html')


def refund_policy(request):
    return render(request, 'main/refund_policy.html')


@login_required
def approved_users(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    approved_users = MatrimonyApplication.objects.filter(is_approved=True)
    return render(request, 'main/approved_users.html', {'normal_user': approved_users})


@login_required
def rejected_users(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    rejected_users = MatrimonyApplication.objects.filter(is_rejected=True)
    return render(request, 'main/rejected_users.html', {'normal_user': rejected_users})


@login_required
def active_users(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    active_users = MatrimonyApplication.objects.filter(is_approved=True, status='Active')
    return render(request, 'main/active_users.html', {'normal_user': active_users})


@login_required
def inactive_users(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    inactive_users = MatrimonyApplication.objects.filter(is_approved=True, status='Inactive')
    return render(request, 'main/inactive_users.html', {'normal_user': inactive_users})


@login_required
def blocked_users(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    blocked_users = MatrimonyApplication.objects.filter(status='Blocked')
    return render(request, 'main/blocked_users.html', {'normal_user': blocked_users})


@login_required
def unpaid_apps(request):
    if not request.user.is_staff:
        return render(request, 'main/404.html')
    unpaid_apps = MatrimonyApplication.objects.filter(is_approved=False, is_paid=False, status='Active')
    return render(request, 'main/unpaid_users.html', {'normal_user': unpaid_apps})


@login_required
def settle_app(request, id):
    try:
        app: MatrimonyApplication = MatrimonyApplication.objects.get(id=id)
        if request.user.matrimonyapplication == app:
            app.status = "Inactive"
            app.is_settled = True
            app.save()
    except:
        pass
    finally:
        return redirect('profile', request.user.email)


@login_required
def admin_settle_app(request, id):
    try:
        app: MatrimonyApplication = MatrimonyApplication.objects.get(id=id)
        if request.user.is_staff:
            app.status = "Inactive" if app.status == 'Active' else 'Active'
            app.is_settled = not app.is_settled
            app.save()
    except:
        return render(request, 'main/404.html')
    finally:
        return redirect('admin-application-details', app.email)


@csrf_exempt
def complete_submission(request, app_id):
    # try:
    m: MatrimonyApplication = get_object_or_404(MatrimonyApplication, id=app_id)
    if request.method == "GET":
        context = {
            "is_single": m.marital_status == "Single",
            "is_divorced": m.marital_status == "Divorced",
            "is_widowed": m.marital_status == "Widowed",
            "is_disabled": m.disability == "Yes"
        }
        return render(request, "main/complete_sub.html", context=context)
    else:
        instance = m
        deletion_dict = {
            'passport_photo': instance.passport_photo.public_id if instance.passport_photo is not None else None,
            'family_photo': instance.family_photo.public_id if instance.family_photo is not None else None,
            'your_photo_1': instance.your_photo_1.public_id if instance.your_photo_1 is not None else None,
            'your_photo_2': instance.your_photo_2.public_id if instance.your_photo_2 is not None else None,
            'your_photo_3': instance.your_photo_3.public_id if instance.your_photo_3 is not None else None,
        }
        form = FilesForm(request.POST, request.FILES, instance=m)
        if form.is_valid():
            m = form.save()
            for i in deletion_dict.keys():
                if i in form.changed_data:
                    if deletion_dict[i] is not None:
                        status = cloudinary.uploader.destroy(deletion_dict[i], invalidate=True)
            subject = "New Registration"
            html_content = get_template(
                'main/new_mail_approval.html').render({'app': instance})
            mail = EmailMultiAlternatives(subject, html_content, from_email="welcome@marryacatholic.com", to=[
                "marryacatholic@gmail.com"])
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
            for k, v in request.FILES.items():
                mail.attach(
                    f'{k}.{v.name.split(".")[-1]}', v.read(), v.content_type)
            mail.send()
            context = {
                "is_single": m.marital_status == "Single",
                "is_divorced": m.marital_status == "Divorced",
                "is_widowed": m.marital_status == "Widowed",
                "is_disabled": m.disability == "Yes"
            }
            return render(request, "main/complete_sub.html", context=context)
        else:
            return render(request, 'main/404.html')


# except Http404 as e:
#     return render(request, 'main/404.html')

def carousel(img):
    return f'/media/{img}' if img else '/media/56117400-9a911800-5f85-11e9-878b-3f998609a6c8_pnb08c.jpg'


def image_preview(request, index, img_no):
    app = MatrimonyApplication.objects.get(id=index)
    if img_no == '0':
        return render(request, 'main/img_preview.html', {'img': carousel(app.family_photo_1)})
    elif img_no == '1':
        return render(request, 'main/img_preview.html', {'img': carousel(app.your_photo_1_1)})
    elif img_no == '2':
        return render(request, 'main/img_preview.html', {'img': carousel(app.your_photo_2_1)})
    elif img_no == '3':
        return render(request, 'main/img_preview.html', {'img': carousel(app.your_photo_3_1)})
    elif img_no == '4':
        return render(request, 'main/img_preview.html', {'img': carousel(app.passport_photo_1)})
    else:
        return render(request, 'main/img_preview.html', {'img': carousel(None)})


@login_required
def meet_and_greet_creation_page(request):
    if request.method == "GET":
        conn: Connection = Connection.objects.filter(user=request.user.email)[0]
        if not conn:
            return render(request, "main/meet_and_greet_creation_page.html", {'matched_list': None})
        matched_list = conn.matched.all()
        if not matched_list:
            return render(request, "main/meet_and_greet_creation_page.html", {'matched_list': None})
        return render(request, "main/meet_and_greet_creation_page.html", {'matched_list': matched_list})
    else:
        # try:
        other_party = User.objects.filter(email=request.POST.get("other_party"))[0]
        new_request: MeetAndGreetRequest = MeetAndGreetRequest.objects.create(
            booked_by=request.user,
            other_party=other_party,
            meet_date=request.POST.get("meet_date"),
            meet_slot=request.POST.get("meet_slot")
        )

        # * send email to fwc about new request
        # * send affirmation email to 'booked_by', request was submitted, you'll be notified in a few days.
        subject = "[Meet & Greet] New Request"
        html_content = get_template(
            'main/mail_meet_request_to_admin.html').render({'req': new_request})
        mail = EmailMultiAlternatives(
            subject, html_content, from_email="welcome@marryacatholic.com", to=['fwcbangalore@gmail.com'],
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

        subject = "[Meet & Greet] Request was submitted!"
        html_content = get_template(
            'main/mail_request_success_user.html').render({'req': new_request})
        mail = EmailMultiAlternatives(
            subject, html_content, from_email="welcome@marryacatholic.com", to=[request.user.email],
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

        return redirect('user-dashboard')
    # except:
    #     return HttpResponse('<script>alert("Some error occurred. Please contact site admin at fwcbangalore@gmail.com."); window.history.back();</script>')


@login_required
def meet_and_greet_admin(request):
    meet_greet_requests = MeetAndGreetRequest.objects.all()
    approved_ones = meet_greet_requests.filter(approved=True)
    not_approved_ones = meet_greet_requests.filter(approved=False)

    context = {
        "requests": meet_greet_requests,
    }

    return render(request, 'main/meet_and_greet_admin.html', context)


@login_required
def meet_and_greet_admin_edit(request, id):
    req = MeetAndGreetRequest.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'main/meet_and_greet_edit.html', {"req": req})
    else:
        req.meet_date = request.POST.get("meet_date")
        req.meet_slot = request.POST.get("meet_slot")
        req.approved = True
        req.save()
        subject = "[Meet & Greet] Request Approved"

        html_content = get_template(
            'main/mail_meet_request_approved.html').render({'req': req})
        mail = EmailMultiAlternatives(
            subject, html_content, from_email="welcome@marryacatholic.com", to=[req.booked_by.email],
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
        return redirect('meet-and-greet-admin')
