from django.shortcuts import redirect, render, get_object_or_404
from .models import Alarm, Notification
from .tasks import schedule_alarm
from django.contrib import messages
import requests
from datetime import datetime
import json
from django.conf import settings

with open(str(settings.BASE_DIR)+'/config.json') as f:
   key_data = json.load(f)

# helper functions

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key_data['weather_api_key']}"
    r = requests.get(url).json()
    weather = {
    'city' : city,
    'temperature' : r['main']['temp'],
    'description' : r['weather'][0]['description'],
    'icon' : r['weather'][0]['icon'],
    }
    return weather

def get_news_data(q):
    url = f"https://newsapi.org/v2/top-headlines?q={q}&apiKey={key_data['news_api_key']}"
    r = requests.get(url).json()
    alarm = Alarm.objects.all()
    news = []
    for i in range(len(alarm)):
        news.append({
        'title':r['articles'][i]['title'],
        'url':r['articles'][i]['url']
        })
    return news


# app views

def home_view(request):
    alarm_list = Alarm.objects.all().order_by('timestamp_to')
    notification_list = Notification.objects.all()
    weather = get_weather_data('Indore')
    news = get_news_data('India')

    context = {'favicon':'https://cdn.iconscout.com/icon/premium/png-256-thumb/smart-alarm-clock-1963840-1657470.png',
                'title':"HELLO WORLD",
                'alarm_list':zip(alarm_list,news),
                'notification_list':notification_list,
                'weather':weather,
            }
    return render(request, 'home.html', context)

def create_alarm(request):
    now = datetime.strptime(str(request.GET.get('alarm')).replace('T', ' ')+":00", '%Y-%m-%d %H:%M:%S')
    
    if now > datetime.now():
        alarm = Alarm.objects.create(title=request.GET.get('title'), 
                                    label=request.GET.get('two'), 
                                    news=False if request.GET.get('news') == None else True,
                                    weather=False if request.GET.get('weather') == None else True)
        alarm.save()
        messages.success(request, "Alarm has been set successfully!")
    else:
        messages.warning(request, "Please enter a valid time!")

    return redirect('home-view')

def delete_alarm(request):
    obj = get_object_or_404(Alarm, pk=request.GET.get('alarm_item'))
    obj.delete()
    return redirect('home-view')

def notification_clear(request):
    obj = get_object_or_404(Notification, title=request.GET.get('notification_item'))
    obj.delete()
    return redirect('home-view')