from django.shortcuts import render
from facebook import *
from models import *
from django.http import HttpResponse
from flask import g, render_template, redirect, request, session

from .models import Greeting
#from app import *

id_app = '470878943108446'
app_secret = '3954f1938f5936e9d6daa85868ffdefe'

#@app.route('/')
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

#@app.route('/login')
def fblogin(request):
    if 'user' in request.session or 'token' in request.session or 'token' in request.POST:
        return fb_profile(request)
    return render(request, 'fblogin.html')

#@app.route('/profile')
def fb_profile(request):
    token = -1


    if 'token' not in request.POST and 'token' not in request.session:
        return render(request, 'fblogin.html')

    if 'token' in request.session:
        token = request.session['token']
    if 'token' in request.POST:
        token = request.POST['token']

    if not 'user' in request.session:
        user = User()
        graph = GraphAPI(token);
        args = {'fields':'id,name,email,birthday'}
        me = graph.get_object('me', **args)
        user.id=me['id']
        user.name = me['name']
        user.email = me['email']
        user.birthday = me['birthday']
        if not User.objects.filter(id=user.id).exists():
            user.save()
        request.session['user'] = user
    request.session['token'] = token
    #if Photo.objects.filter(id_owner = user.id).exists():
    photos = Photo.objects.filter(id_owner = user.id)
    return render(request, 'profile.html', {'person' : user, 'photos' : photos })

def fbphotos(request):
    if 'user' not in request.session or 'token' not in request.session:
        return fblogin(request)

    request.session['token'] = 'CAACEdEose0cBAOKTRNIdlZCCMQGKtdDAKh8ZBRr1NXnZAZBLHOwLOzmmUiZAfZBRNfnJ3TqeKOmccnUsxy2GRYumVowG9620TgFKFVu0LEKZAiUdBtlFeebibMgi4XxFXMaHmLNM8ZCCKLhlfRBKy35asqrqEln6XJr3ZBHaCRpvVNEFRnnkQeXC3ZCuIc7ZAjfZCBRt7aMJq3XozAZDZD'
    graph = GraphAPI(request.session['token'])
    args = {'type':'uploaded'}
    photos = graph.get_connections(id='me', connection_name='photos', **args)
    user = request.session['user']
    if photos is not None:
        for photo in photos['data']:
            fbphoto = Photo()
            fbphoto.id = photo['id']
            fbphoto.id_owner = user
            if 'name' in photo:
               fbphoto.name = photo['name']
            if 'created_time' in photo:
                fbphoto.created_time = photo['created_time']
            if Photo.objects.filter(id=fbphoto.id).count() <= 0:
                fbphoto.save()

    return render(request, 'profile.html', {'person' : user, 'photos' : photos['data'] })


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

