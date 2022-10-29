from django.contrib import admin
from .models import Alarm, Notification

admin.site.register(Alarm)
admin.site.register(Notification)