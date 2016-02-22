import requests
from django.shortcuts import *
from django.http import HttpResponseRedirect
from models import *

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'

def login(request):
    redirect_uri = 'https://facebookalgorithm.herokuapp.com/instagram/profile'
    url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code'
    r = requests.get('url')
    return render(request, 'instagram_login.html', {'info':r})

def profile(request):
    return render(request, 'instagram_profile.html')