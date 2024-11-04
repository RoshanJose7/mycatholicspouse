from django.shortcuts import render
from django.contrib.auth.views import login_required

from .models import MatrimonyApplication
from .matchmaking import MatchMaker
from .faker_test import lang_list
from .models import Connection

m = MatchMaker()

@login_required(login_url = 'login')
def user_dashboard(request):
    # user_application = request.user.user_application
    user_application = request.user.matrimonyapplication
    if user_application.status != 'Active':
        return render(request, "main/404.html")
    if request.method == "GET":
        m.make_match(user_application)
        context = {
            "user": user_application,
            "recommended_users": m.all_apps,
            "lang_list": lang_list,
        }
    else:
        t = user_application
        if (request.POST.get("dash") == "1"):
            m.get_results(t, request.POST)
        else:
            m.get_results_from_homepage(t, request.POST)
        context = {
            "user": t,
            "recommended_users": m.set_q,
            "lang_list": lang_list,
        }

    return render(request, "main/user_dash.html", context)

@login_required(login_url = 'login')
def user_detail_view(request, id):
    user_app = MatrimonyApplication.objects.get(id=id)
    if user_app.status != 'Active' or request.user.matrimonyapplication.status != 'Active':
        return render(request, "main/404.html")
    user_connection, _ = Connection.objects.get_or_create(
        user=request.user.email)
    if request.user in user_connection.was_blocked.all():
        return render(request, "main/404.html")
    context = {
        'user_app': user_app,
        'has_liked': user_app.user in user_connection.has_liked.all() or user_app.user in user_connection.matched.all(),
        'has_unliked': user_app.user in user_connection.has_unliked.all(),
        'matched': user_app.user in user_connection.matched.all(),
        'has_blocked': user_app.user in user_connection.has_blocked.all(),
    }
    return render(request, 'main/user_view.html', context)

@login_required(login_url = 'login')
def admin_user_detail_view(request, id):
    user_app = MatrimonyApplication.objects.get(id=id)
    if request.user.is_staff:
        if user_app.passport_photo is None:
            if user_app.gender == "Male":
                t = "https://bootdey.com/img/Content/avatar/avatar7.png"
            else:
                t = "https://www.bootdey.com/img/Content/avatar/avatar3.png"
        else:
            t = user_app.passport_photo.url.split("/")
            t = "/".join(t[:-2]) + "/w_500,h_500,c_fill/" + "/".join(t[-2:])
        context = {
            'user_app': user_app,
            'passport_photo': t,
            'has_liked': True,
            'has_unliked': True,
            'matched': True,
            'has_blocked': True,
        }
        return render(request, 'main/user_view.html', context)
    else:
        return render(request, 'main/404.html')

def show_has_liked(request):
    try:
        if MatrimonyApplication.objects.get(email = request.user.email).status != 'Active':
            return render(request, "main/404.html")
    except:
        return render(request, "main/404.html")
    try:
        conn, _ = Connection.objects.get_or_create(user=request.user.email)
        has_liked_list = conn.has_liked.all()
    except:
        has_liked_list = None
        print(has_liked_list, "except")
    context = {
        'has_liked_list': has_liked_list,
    }
    return render(request, "main/has_liked.html", context)


def show_was_liked(request):
    try:
        if MatrimonyApplication.objects.get(email = request.user.email).status != 'Active':
            return render(request, "main/404.html")
    except:
        return render(request, "main/404.html")
    try:
        conn, _ = Connection.objects.get_or_create(user=request.user.email)
        was_liked_list = conn.was_liked.all()
    except:
        was_liked_list = None
    print(was_liked_list)
    context = {
        'was_liked_list': was_liked_list,
    }
    return render(request, "main/was_liked.html", context)


def show_matched(request):
    try:
        if MatrimonyApplication.objects.get(email = request.user.email).status != 'Active':
            return render(request, "main/404.html")
    except:
        return render(request, "main/404.html")
    try:
        conn, _ = Connection.objects.get_or_create(user=request.user.email)
        matched_list = conn.matched.all()
    except:
        matched_list = None
    context = {
        'matched_list': matched_list,
    }
    return render(request, "main/matched.html", context)

def show_not_interested(request):
    try:
        if MatrimonyApplication.objects.get(email = request.user.email).status != 'Active':
            return render(request, "main/404.html")
    except:
        return render(request, "main/404.html")
    try:
        conn, _ = Connection.objects.get_or_create(user=request.user.email)
        has_unliked_list = conn.has_unliked.all()
    except:
        has_unliked_list = None
    context = {
        'has_unliked_list': has_unliked_list,
    }
    return render(request, "main/has_unliked.html", context)

def show_blocked(request):
    try:
        if MatrimonyApplication.objects.get(email = request.user.email).status != 'Active':
            return render(request, "main/404.html")
    except:
        return render(request, "main/404.html")
    try:
        conn, _ = Connection.objects.get_or_create(user=request.user.email)
        has_blocked_list = conn.has_blocked.all()
    except:
        has_blocked_list = None
    context = {
        'has_blocked_list': has_blocked_list,
    }
    return render(request, "main/has_blocked.html", context)

