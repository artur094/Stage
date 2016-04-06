import requests
from django.http import HttpResponseRedirect
from django.shortcuts import *
from my_class.instagram import Instagram

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'
redirect_uri = 'https://facebookalgorithm.herokuapp.com/instagram/token'

self_users_url = 'https://api.instagram.com/v1/users/self/'

#login for instagram app
def login(request):
    permissions = 'scope=basic+follower_list+relationships+likes+public_content'
    url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code&'+permissions
    return HttpResponseRedirect(url)

#recupero token
def token(request):
    if 'error' not in request.GET and 'code' not in request.GET:
        return login(request)
    if 'error' in request.GET:
        return HttpResponse("Errore")

    url = 'https://api.instagram.com/oauth/access_token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': request.GET['code'],
    }
    my_data = requests.post(url, data=data)

    if 'error_type' in my_data.json() or 'error_message' in my_data.json():
        return login(request)

    request.session['inst_token'] = my_data.json()['access_token']

    return profile(request)


def profile(request):
    if 'inst_token' not in request.session:
        login(request)

    token = request.session['inst_token']

    # now I have the token

    inst = Instagram()

    if 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 'self'

    my_profile = inst.profile(id, token)
    my_posts = inst.posts(id, token)

    #liked = requests.get(self_users_url+'media/liked', token)

    return render(request, 'social/instagram_profile.html', {'profile': my_profile, 'posts':my_posts, 'token':token})

def search(request):
    return render(request, 'social/instagram_profile.html')

def hashtags(request):
    return render(request, 'social/instagram_profile.html')

def follows(request):
    if 'token' not in request.session:
        return login(request)

    data = {
        'access_token': request.session['inst_token']
    }
    r = requests.get(self_users_url+'follows',data)
    return render(request, 'social/instagram_follows.html', {'dati':r.json()})

def followedby(request):
    if 'token' not in request.session:
        return login(request)

    data = {
        'access_token': request.session['inst_token']
    }
    r = requests.get(self_users_url+'followed_by',data)
    return render(request, 'social/instagram_follows.html', {'dati':r.json()})