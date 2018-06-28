from django.contrib import admin
from leave.models import LeaveRules,LeaveApply
# Register your models here.
admin.site.register(LeaveRules)
admin.site.register(LeaveApply)
