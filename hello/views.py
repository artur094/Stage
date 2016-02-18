from django.shortcuts import render
from facebook import *
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
    return render(request, 'fblogin.html')

#@app.route('/profile')
def fb_profile(request):
    return  render(request, 'profile.html')

def test(request):
    prova = 54
    return render(request, 'profile.html', {'person' : prova })

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

