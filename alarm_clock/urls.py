from django.urls import path
from .views import home_view, create_alarm, delete_alarm, notification_clear

urlpatterns = [
    path('', home_view, name='home-view'),
    path('submit/', create_alarm, name='create-alarm-view'),
    path('delete_alarm/', delete_alarm, name='delete-alarm-view'),
    path('notification-clear/', notification_clear, name='notification-clear-view'),
]
