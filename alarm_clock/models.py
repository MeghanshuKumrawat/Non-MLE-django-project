from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Alarm(models.Model):
    title = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    news = models.BooleanField(default=True)
    weather = models.BooleanField(default=True)
    timestamp_from = models.DateTimeField(auto_now_add=True)
    timestamp_to = models.DateTimeField(blank=True, null=True)
    
    