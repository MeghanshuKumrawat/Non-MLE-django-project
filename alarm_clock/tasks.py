from celery import shared_task
import time
from .models import Alarm
import sched
import pyttsx3

s = sched.scheduler(time.time, time.sleep)

# helper functions 
def invoke_announcement(a):
    obj = pyttsx3.init()
    obj.say(a)
    obj.runAndWait()  

@shared_task()
def schedule_alarm():
    while True:
        alarm_list = Alarm.objects.all().order_by('timestamp_to')
        print('----------------------------', 'task started')
        for alarm in alarm_list:
            print(alarm.timestamp_to)
            st = str(alarm.timestamp_to).split('+')[0]
            t = time.strptime(st, '%Y-%m-%d %H:%M:%S')
            t = time.mktime(t)
            s.enter(t, 1, invoke_announcement, argument=('hey, weak up',))
            s.run()
    print('----------------------------', 'task end')


