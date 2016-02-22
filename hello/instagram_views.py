import requests
from django.shortcuts import *
from django.http import HttpResponseRedirect
from instagram.client import InstagramAPI
from models import *

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'

def login(request):
    redirect_uri = 'https://facebookalgorithm.herokuapp.com/instagram/'
    if 'error' not in request.GET and 'code' not in request.GET:
        url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code'
        return HttpResponseRedirect(url)
    elif 'error' in request.GET:
        return HttpResponse("ERROR")
    elif 'code' in request.GET :
        url = 'https://api.instagram.com/oauth/access_token'
        data = {
            'client_id': client_id,
            'client_secret':client_secret,
            'grant_type':'authorization_code',
            'redirect_uri':redirect_uri,
            'code':request.GET['code']
        }
        r = requests.get(url, params=data)
        return render(request, 'instagram_profile.html', {'token':r.json()})
    else:
        return HttpResponse("ERROR")





def profile(request):
    token = request.GET['code']
    api = InstagramAPI(access_token=token, client_secret=client_secret)
    return render(request, 'instagram_profile.html', {'token':token})