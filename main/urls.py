from django.urls import path, include
from . import views
from . import api_views
from . import user_dashboard_views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.home, name="home"),
    path("form-fill-instructions/", views.form_instruction, name="form-fill-instructions"),
    path('matrimony-form/', views.matrimony_form, name="matrimony-form"),
    path('privacy-policy/', views.priv_policy, name="privacy-policy"),
    path('terms-and-conditions/', views.tnc, name="terms-and-conditions"),
    path('sumbit/', api_views.form_submit, name="submit"),
    path("administrator/", include("main.admin_urls")),
    path("api/", include("main.api_urls")),
    path('dj-form/', views.dj_form, name="dj-form"),
    path('login/', LoginView.as_view(template_name='main/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='main/logout.html'), name="logout"),
    path('profile/<email>/', views.profile, name="profile"),
    path('complete-submission/<app_id>/', views.complete_submission, name="complete-submission"),
    path('dashboard/', user_dashboard_views.user_dashboard, name="user-dashboard"),
    path('show-has-liked/', user_dashboard_views.show_has_liked,
         name="show-has-liked"),
    path('show-was-liked/', user_dashboard_views.show_was_liked,
         name="show-was-liked"),
    path('show-matched/', user_dashboard_views.show_matched, name="show-matched"),
    path('show-has-unliked/', user_dashboard_views.show_not_interested, name="show-has-unliked"),
    path('show-blocked/', user_dashboard_views.show_blocked, name="show-blocked"),
    path('user-view/<id>/', user_dashboard_views.user_detail_view, name="user-view"),
    path('admin-user-view/<id>/', user_dashboard_views.admin_user_detail_view, name="admin-user-view"),
    path('login-with-ID/', views.login_ID, name="login-with-ID"),
    path('select-plan/<app_id>/', views.select_plan, name="select-plan"),
    path('update-details/<id>/', views.update_details, name="update-details"),
    path('checkout/<receipt_id>/', views.checkout, name="checkout" ),
    path('about-us/', views.about_us, name="about-us"),
    path('contact-us/', views.contact_us, name="contact-us"),
    path('refund-policy/', views.refund_policy, name="refund-policy"),
    path('settle-app/<id>/', views.settle_app, name="settle-app"),
    path('password-reset/', views.password_reset, name="password-reset"),
    path('password-reset-next/<token>/', views.password_reset_next, name='password-reset-next'),
    path('image-preview/<index>/<img_no>/', views.image_preview, name="image-preview"),
    path('meet-and-greet/', views.meet_and_greet_creation_page, name="meet-and-greet"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


