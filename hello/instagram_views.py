from django.shortcuts import *
from django.http import HttpResponseRedirect
from instagram.client import InstagramAPI
from models import *

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'

def login(request):
    redirect_uri = 'https://facebookalgorithm.herokuapp.com/instagram/profile'
    url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code'
    return HttpResponseRedirect(url)

def profile(request):
    token = request.GET['code']
    api = InstagramAPI(access_token=token, client_secret=client_secret)
    return render(request, 'instagram_profile.html', {'token':token})