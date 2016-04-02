from django.shortcuts import render
from facebook import *
from models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from flask import g, render_template, redirect, request, session
from lxml import html
import requests
from splinter import Browser
from my_class.comune_matrimoni import Matrimoni



import my_class.instagram

hashtags = ['italy','sposi', 'matrimonio', 'nozze', 'mariage', 'matrimoni']

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'
redirect_uri = 'https://facebookalgorithm.herokuapp.com/profile'
scope = 'public_content'
self_users_url = 'https://api.instagram.com/v1/users/self/'


def matrimoni(request):
    mat = Matrimoni()
    vettore_sposi = []
    vettore_sposi.extend(mat.trento())
    vettore_sposi.extend(mat.pergine())

    return render(request, 'index.html', {'sposi': vettore_sposi})

def login(request):
    permissions = 'scope=basic+follower_list+relationships+likes+public_content'
    url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code&'+permissions
    return HttpResponseRedirect(url)

def profile(request):
    if 'error' not in request.GET and 'code' not in request.GET:
        return login(request)
    if 'error' in request.GET:
        return HttpResponse("Errore")

    url = 'https://api.instagram.com/oauth/access_token'
    data = {
        'client_id': client_id,
        'client_secret':client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri':redirect_uri,
        'code':request.GET['code'],
    }
    profile = requests.post(url,data=data)

    if 'error_type' in profile.json() or 'error_message' in profile.json():
        return login(request)

    request.session['inst_token'] = profile.json()['access_token']
    token = {'access_token': profile.json()['access_token']}

    #liked = requests.get(self_users_url+'media/liked', token)
    inst = my_class.instagram.Instagram()
    return render(request, 'social/instagram_profile.html', {'dati':inst.post_hashtags(hashtags, token['access_token']), 'token':token['access_token']})


