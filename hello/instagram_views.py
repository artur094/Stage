from django.shortcuts import render
from models import *

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'

def login(request):
    url_inst = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='
    url_profile = 'https://facebookalgorithm.herokuapp.com/instagram_profile'
    url = url_inst+url_profile+'&response_type=token'
    return render(request, 'instagram_login.html', {'url': url})

def profile(request):
    return render(request, 'instagram_profile.html')