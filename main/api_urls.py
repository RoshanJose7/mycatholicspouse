from django.urls import path

from . import api_views

urlpatterns = [
    path("approve-user/<email>/", api_views.approve_user, name="approve-user"),
    path("reject-user/", api_views.rejection_admin, name="reject-user"),
    path("batch-approval/", api_views.batch_approval, name="batch-approval"),
    path("edit-profile/<email>/", api_views.edit_profile, name="edit-profile"),
    path("admin-edit-profile/<email>/",
         api_views.admin_edit_profile, name="admin-edit-profile"),
    path('like/<id>/', api_views.liked, name="like-app"),
    path('dislike/<id>/', api_views.disliked, name="dislike-app"),
    path('unlike/<id>/', api_views.unliked, name="unlike-app"),
    path('disunlike/<id>/', api_views.disunliked, name="disunlike-app"),
    path('block/<id>/', api_views.blocked, name="block-app"),
    path('disblock/<id>/', api_views.disblocked, name="disblock-app"),
    path('check-cred/<str:reg_id>/<str:password>/',
         api_views.check_cred, name="check-cred"),
    path('update-profile-id/<id>/',
         api_views.update_profile_id, name="update-profile-id"),
    path('order-generate/<receipt_id>/',
         api_views.order_generate, name="order-generate"),
    path('switch-status/<email>/<status>/',
         api_views.switch_status, name='switch-status'),
    path('check-status/<email>/', api_views.check_status, name='check-status'),
    path('php-call-api/', api_views.php_call_api, name="php-call-api"),
    path('users2csv/', api_views.users2csv, name='users2csv')
]
