from django.shortcuts import render
from facebook import *
from models import *
from django.db.models import Q
from django.http import HttpResponse
from flask import g, render_template, redirect, request, session

from .models import Greeting
#from app import *

id_app = '470878943108446'
app_secret = '3954f1938f5936e9d6daa85868ffdefe'
token_tmp = 'CAACEdEose0cBALsUSPi9bonydKH383bYZBhq8MAA2gvsGYXtXx57BB0zmdQqecQVbLVmQk2k8yazn0cDfJseVjrGQR40ZCJYWk3RqtcxWyXJiRjayaSZCPp5ezyJOjEO0O115RBSjnl4BngPPOVygN3VhetjwjZB3JFpvEsdmuDZAz05MH3MStmR8maJ9GZAaGA05o7tj7RgZDZD'

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


    if 'token' not in request.POST and 'token' not in request.session:
        return render(request, 'fblogin.html')

    if 'token' in request.session:
        token = request.session['token']
    if 'token' in request.POST:
        token = request.POST['token']

    if not 'user' in request.session:
        user = User()
        graph = GraphAPI(token);
        args = {'fields':'id,name,email,birthday'}
        me = graph.get_object('me', **args)
        user.id=me['id']
        user.name = me['name']
        user.email = me['email']
        if 'birthday' in me:
            user.birthday = me['birthday']
        if not User.objects.filter(id=user.id).exists():
            user.save()
        request.session['user'] = user
    else:
        user = request.session['user']

    request.session['token'] = token

    fbphotos(request)
    fbfriends(request)
    #fbposts(request)

    #if Photo.objects.filter(id_owner = user.id).exists():
    photos = Photo.objects.filter(id_owner = user.id)
    friends = Friend.objects.filter(user = user.id)
    posts = Post.objects.filter(id_creator = user.id)
    return render(request, 'profile.html', {'token':token,'person' : user, 'photos' : photos, 'friends':friends, 'posts':posts })

def fbphotos(request):
    if 'user' not in request.session or 'token' not in request.session:
        return fblogin(request)

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
               fbphoto.name = photo['name']
            if 'created_time' in photo:
                fbphoto.created_time = photo['created_time']
            if Photo.objects.filter(id=fbphoto.id).count() <= 0:
                fbphoto.save()

    #return render(request, 'profile.html', {'person' : user, 'photos' : photos['data'] })

def fbfriends(request):
    if 'user' not in request.session or 'token' not in request.session:
        return fblogin(request)

    user = request.session['user']
    token = request.session['token']
    graph = GraphAPI(token)
    #token = token_tmp
    friends = graph.get_connections(id='me', connection_name='friends')

    for friend in friends['data']:
        fbfriend = Friend()
        fbfriend.user = user;
        if User.objects.filter(id=friend['id']).exists():
            user_friend = User.objects.get(id=friend['id'])
        else:
            user_friend = User()
            user_friend.id = friend['id']
            user_friend.name = friend['name']
            user_friend.save()
        fbfriend.friend = user_friend
        if not Friend.objects.filter(user=fbfriend.user).filter(friend=fbfriend.friend).exists():
            #return HttpResponse("User: "+fbfriend.user.id+"<br />Friend: "+fbfriend.friend.id)
            fbfriend.save()

    #return render(request, 'test.html', {'friends':friends, 'token':token})
    #return fb_profile(request)

def fbposts(request):
    if 'user' not in request.session or 'token' not in request.session:
        return fblogin(request)

    user = request.session['user']
    token = request.session['token']
    graph = GraphAPI(token)

    args = {'fields':'story,created_time,id,description,type,to'}
    posts = graph.get_connections(id='me', connection_name='posts',**args)
    for post in posts['data']:
        p = Post()
        p.id_post = post['id']
        p.id_creator = user
        if 'created_time' in post:
            p.date = post['created_time']
        if 'story' in post:
            p.story = post['story']
        if 'description' in post:
            p.description = post['description']
        if 'type' in post:
            p.type = post['type']
        if 'to' in post:
            id_user = post['to']['data']['id']
            name_user = ((post['to'])['data'])['name']
            if User.objects.filter(id = id_user):
                to_user = User.objects.filter(id = id_user)
            else:
                to_user = User()
                to_user.id = id_user
                to_user.name = name_user
                to_user.save()
            p.to = to_user
        else:
            p.to = user

        if not Post.objects.filter(id_post=p.id_post).exists():
            p.save()
    return render(request, 'test.html', {'posts': posts['data']})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

