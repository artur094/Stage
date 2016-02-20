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
    if 'user' in request.session:
        return render(request, 'profile.html', {'person' : request.session['user'] })

    if 'token' not in request.POST and 'token' not in request.session:
        return render(request, 'fblogin.html')

    if 'token' in request.session:
        token = request.session['token']
    if 'token' in request.POST:
        token = request.POST['token']

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
    if Photo.objects.filter(id_owner = user.id).exists():
        photos = Photo.objects.get(id_owner = user.id)
    else:
        photos = None
    return render(request, 'profile.html', {'person' : user, 'photos' : photos })

def fbphotos(request):
    if 'user' not in request.session or 'token' not in request.session:
        return fblogin(request)

    request.session['token'] = 'CAACEdEose0cBAHrm6zAaF06AfufUU4FXtx6SE3A19ZCFZBDJPd8ezYJZCKQ89RMF6CPAKbPDjJZAPAoTAGGcNO9POZB9i50FvLhXEogz2eElvC6WNrHcWG61XFf88wU4QSMIpfZCj34NZAXI1rAEZCMDEgf31jZBFhotQfK9DgYF7AyPB9w9QwPuGZB455rxgVtWEzRnQG3BgRTQZDZD'
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
                fbphoto.message = photo['name']
            if 'created_time' in photo:
                fbphoto.date = photo['created_time']
            if not Photo.objects.filter(id=fbphoto.id).exists():
                fbphoto.save()

    return render(request, 'profile.html', {'person' : user, 'photos' : photos })


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

