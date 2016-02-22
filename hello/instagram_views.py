import requests
import json
from django.shortcuts import *
from django.http import HttpResponseRedirect
from instagram.client import InstagramAPI
from models import *

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'
redirect_uri = 'https://facebookalgorithm.herokuapp.com/instagram/profile'

self_users_url = 'https://api.instagram.com/v1/users/self/'

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

    request.session['token'] = profile.json()['access_token']
    token = {'access_token': profile.json()['access_token']}

    liked = requests.get(self_users_url+'media/liked', token)

    return render(request, 'instagram_profile.html', {'dati':profile.json(), 'liked':liked})

def follows(request):
    if 'token' not in request.session:
        return login(request)

    data = {
        'access_token': request.session['token']
    }
    r = requests.get(self_users_url+'follows',data)
    return render(request,'instagram_follows.html', {'dati':r.json()})

def followedby(request):
    if 'token' not in request.session:
        return login(request)

    data = {
        'access_token': request.session['token']
    }
    r = requests.get(self_users_url+'followed_by',data)
    return render(request,'instagram_follows.html', {'dati':r.json()})