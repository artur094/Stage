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

    user = Utente()
    graph = GraphAPI(token);
    args = {'fields':'id,name,email,birthday'}
    me = graph.get_object('me', **args)
    user.id=me['id']
    user.name = me['name']
    user.email = me['email']
    user.birthday = me['birthday']
    if Utente.objects.filter(id=user.id).exists():
        user.save()
    request.session['user'] = user
    request.session['token'] = token
    return render(request, 'profile.html', {'person' : user })

def test(request):
    user = Utente()
    token = request.POST['token']
    graph = GraphAPI(token);
    args = {'fields':'id,name,email,birthday'}
    me = graph.get_object('me', **args)
    user.id=me['id']
    user.name = me['name']
    user.email = me['email']
    user.birthday = me['birthday']
    request.session['user'] = user;

    return render(request, 'profile.html', {'person' : user })

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

