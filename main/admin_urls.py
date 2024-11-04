from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.admin_home, name="admin-home"),
    path('application/<email>/', views.admin_profile_preview,
         name="admin-application-details"),
    path('print-profile/<email>/', views.print_profile_data,
         name="print-profile"),
    path('approved-users/', views.approved_users, name='approved-users'),
    path('rejected-users/', views.rejected_users, name='rejected-users'),
    path('active-users/', views.active_users, name='active-users'),
    path('inactive-users/', views.inactive_users, name='inactive-users'),
    path('blocked-users/', views.blocked_users, name='blocked-users'),
    path('unpaid-users/', views.unpaid_apps, name='unpaid-users'),
    path('admin-settle-app/<id>/', views.admin_settle_app, name='admin-settle-app'),
    path('meet-and-greet-admin/', views.meet_and_greet_admin, name="meet-and-greet-admin"),
    path('meet-and-greet-edit/<id>/', views.meet_and_greet_admin_edit, name="meet-and-greet-edit"),
]
