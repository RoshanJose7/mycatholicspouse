from django.contrib import admin

from daterangefilter.filters import FutureDateRangeFilter

from .models import *

# Register your models here.
class MatrimonyApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'phone_number', 'status', ]
    list_filter = ['is_paid', 'is_blocked', 'status']
    search_fields = ['email', 'id']

    def get_full_name(self, obj: MatrimonyApplication):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = "Name"

class ConnectionAdmin(admin.ModelAdmin):
    filter_horizontal = ('has_liked', 'was_liked', 'matched', 'has_unliked', 'has_blocked', 'was_blocked', 'was_unliked', )
    search_fields = ['user']

class ReceiptAdmin(admin.ModelAdmin):
    search_fields = ['id', 'order_id']

class MeetAndGreetRequestAdmin(admin.ModelAdmin):
    list_display = ['booked_by', 'other_party', 'meet_date', 'meet_slot', 'approved']
    list_filter = ['meet_slot', ('meet_date', FutureDateRangeFilter), 'approved']
    search = ['booked_by', 'other_party']

admin.site.register(MatrimonyApplication, MatrimonyApplicationAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Plan)
admin.site.register(Receipt)
admin.site.register(PasswordResetToken)
admin.site.register(MeetAndGreetRequest, MeetAndGreetRequestAdmin)