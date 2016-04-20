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
import models


import my_class.instagram

hashtags = ['italy','sposi', 'matrimonio', 'nozze', 'mariage', 'matrimoni']

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'
redirect_uri = 'https://facebookalgorithm.herokuapp.com/token'
scope = 'public_content'
self_users_url = 'https://api.instagram.com/v1/users/self/'


def index(request):
    return render(request, 'index.html')

def matrimoni(request):
    mat = Matrimoni()
    #mat.trento()
    #mat.pergine()
    #mat.arco()
    #mat.rovereto()

    sposi = Coppia.objects.all()

    #sposi = mat.pinzolo()

    return render(request, 'matrimoni.html', {'sposi': sposi})

def test_everything(request):
    mat = Matrimoni()

    sposi = mat.pinzolo()

    return render(request, 'test.html', {'test':sposi})

def test(request):
    #mat = Matrimoni()
    #test = mat.rovereto()

    #test = Coppia.objects.all()

    profile = {
        'id':'048284812394',
        'username': 'Gallet',
        'full_name': 'Gallo Fallet',
        'bio':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'profile_picture':'https://scontent.cdninstagram.com/t51.2885-19/s150x150/12907291_1698752453714245_1472481837_a.jpg'
    }

    posts = [
        {
            'images':{
                'standard_resolution':{
                    'url':'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/12120391_621290608020896_488596262_n.jpg?ig_cache_key=MTIxODIwMjY1NjQ0OTEwNTAxNw%3D%3D.2'
                }
            },
            'caption':
                {
                    'created_time':'1459535453',
                    'from':{
                        'full_name': 'Gallo Fallet'
                    },
                    'text':'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?'
                },
            'user_has_liked':False,
            'type':'Image',
            'location':{
                'name':'Arco',
                'longitude':'10.887777778',
                'latitude':'45.921666667',
            },
            'likes':{
                'count':'14'
            },
            'users_in_photo':[
                {
                    'user':{
                        'username': 'Gallet',
                        'full_name':'Gallo Fallet'
                    }
                },
                {
                    'user': {
                        'username': 'Gronka',
                        'full_name': 'Pollo Fellet'
                    }
                },
                {
                    'user': {
                        'username': 'Canga',
                        'full_name': 'Cagur Canger'
                    }
                },
            ],
            'tags':[
                'tag1','tag2','tag3','tag4','tag1','tag2','tag3','tag4'
            ]
        },
        {
            'images': {
                'standard_resolution': {
                    'url': 'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/12383502_1163827196963669_1829705416_n.jpg?ig_cache_key=MTIxODIwNjA1MjkyMDk4NjgzOA%3D%3D.2.l'
                }
            },
            'caption':
                {
                    'created_time': '1459535453',
                    'from': {
                        'full_name': 'Gallo Fallet'
                    },
                    'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?'
                },
            'user_has_liked': False,
            'type': 'Image',
            'location': {
                'name': 'Arco',
                'longitude': '10.887777778',
                'latitude': '45.921666667',
            },
            'likes': {
                'count': '14'
            },
            'users_in_photo': [
                {
                    'user': {
                        'username': 'Gallet',
                        'full_name': 'Gallo Fallet'
                    }
                },
                {
                    'user': {
                        'username': 'Gronka',
                        'full_name': 'Pollo Fellet'
                    }
                },
                {
                    'user': {
                        'username': 'Canga',
                        'full_name': 'Cagur Canger'
                    }
                },
            ],
            'tags': [
                'tag1', 'tag2', 'tag3', 'tag4', 'tag1', 'tag2', 'tag3', 'tag4'
            ]
        }
    ]

    # {% for post in posts %}
    #                 <div>
    #                     <div>Date: {{ post.caption.created_time }}</div>
    #                     <div>Created By: {{ post.caption.from.full_name }}</div>
    #                     <div>Type: {{ post.type }}</div>
    #                     <div>Do I like this? {{ post.user_has_liked }}</div>
    #                     {% if 'name' in post.location %}
    #                         <div>Posto: {{ post.location.name }}</div>
    #                     {% endif %}
    #                     {% if 'latitude' in post.location and 'longitude' in post.location %}
    #                         <div>Location: Longitudine: {{ post.location.longitude }} - Latitudine: {{ post.location.latitude }}</div>
    #                     {% endif %}
    #                     <div>Testo: {{ post.caption.text }}</div>
    #                     <div>Likes: {{ post.likes.count }}</div>
    #                     <ul>
    #                         {% for user in post.users_in_photo %}
    #                             <li>{{ user.user.username }} - {{ user.user.full_name }}</li>
    #                         {% endfor %}
    #                     </ul>
    #                     <div>
    #                         Tag:
    #                         <div>
    #                             <ul>
    #                                 {% for tag in post.tags %}
    #                                     {{ tag }},
    #                                 {% endfor %}
    #                             </ul>
    #                         </div>
    #                     </div>
    #                 </div>
    #                 <hr />
    #             {% endfor %}


    return render(request, 'social/instagram_profile.html', {'token': 'token', 'profile':profile, 'posts':posts})

def test_search(request):
    users = [
        {
            'username': 'Galloway',
            'profile_picture':'https://scontent.cdninstagram.com/t51.2885-19/11906329_960233084022564_1448528159_a.jpg',
            'id':'',
            'first_name':'Gallo',
            'last_name':'Galloper'
        },
        {
            'username': 'Galloway',
            'profile_picture': 'https://scontent.cdninstagram.com/t51.2885-19/11906329_960233084022564_1448528159_a.jpg',
            'id': '',
            'first_name': 'Gallo',
            'last_name': 'Galloper'
        },
        {
            'username': 'Galloway',
            'profile_picture': 'https://scontent.cdninstagram.com/t51.2885-19/11906329_960233084022564_1448528159_a.jpg',
            'id': '',
            'first_name': 'Gallo',
            'last_name': 'Galloper'
        },
        {
            'username': 'Galloway',
            'profile_picture': 'https://scontent.cdninstagram.com/t51.2885-19/11906329_960233084022564_1448528159_a.jpg',
            'id': '',
            'first_name': 'Gallo',
            'last_name': 'Galloper'
        },
        {
            'username': 'Galloway',
            'profile_picture': 'http://www.filastrocche.it/contenuti/wp-content/uploads/2002/01/gallo-400.jpg',
            'id': '',
            'first_name': 'Gallo',
            'last_name': 'Galloper'
        },
    ]
    return render(request, 'social/instagram_results.html',{'users':users})

def login(request):
    permissions = 'scope=basic+follower_list+relationships+likes+public_content'
    url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code&'+permissions
    return HttpResponseRedirect(url)

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

    return video(request)

def profile(request):
    if 'inst_token' not in request.session:
        login(request)

    token = request.session['inst_token']

    # now I have the token

    inst = my_class.instagram.Instagram()

    if 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 'self'

    my_profile = inst.profile(id, token)
    my_posts = inst.posts(id, token)

    #liked = requests.get(self_users_url+'media/liked', token)

    return render(request, 'social/instagram_profile_2.html', {'profile': my_profile, 'posts':my_posts, 'token':token})

def insta_hashtag(request):
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
    profile = requests.post(url, data=data)

    if 'error_type' in profile.json() or 'error_message' in profile.json():
        return login(request)

    request.session['inst_token'] = profile.json()['access_token']
    token = {'access_token': profile.json()['access_token']}

    # liked = requests.get(self_users_url+'media/liked', token)
    inst = my_class.instagram.Instagram()
    return render(request, 'social/instagram_profile_2.html', {'dati': inst.search_hashtags_intersect(hashtags, token['access_token']), 'token': token['access_token']})

def insta_search(request):
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
    profile = requests.post(url, data=data)

    if 'error_type' in profile.json() or 'error_message' in profile.json():
        return login(request)

    request.session['inst_token'] = profile.json()['access_token']
    token = {'access_token': profile.json()['access_token']}

    # liked = requests.get(self_users_url+'media/liked', token)
    inst = my_class.instagram.Instagram()
    return render(request, 'social/instagram_profile_2.html',
                  {'dati': inst.search_hashtags_intersect(hashtags, token['access_token']), 'token': token['access_token']})

def insta_posts(request):
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
    profile = requests.post(url, data=data)

    if 'error_type' in profile.json() or 'error_message' in profile.json():
        return login(request)

    request.session['inst_token'] = profile.json()['access_token']
    token = {'access_token': profile.json()['access_token']}

    # liked = requests.get(self_users_url+'media/liked', token)
    inst = my_class.instagram.Instagram()
    return render(request, 'social/instagram_profile_2.html',
                  {'dati': inst.posts('2320686410', token['access_token']), 'token': token['access_token']})

def video(request):
    dati = [
        {
            'type': 'image',
            'caption': {
                'from':{
                    'username': 'Giorgio'
                },
                'created_time': '22 Aprile 2016',
                'text': 'Matrimonio con Lucia #nozze, #matrimonio, #nonsochehashtags',
            },
            'location':{
                'name':'Trento'
            },
            'likes':{
                'count':'24'
            },
            'images':{
                'standard_resolution':{
                    'url':'http://www.fotografi-matrimonio.com/padova-galleria-foto-fotoste-di-stefania-chiereghin/images/07-Foto-sposi-in-Chiesa-Santa-Giustina-Pernumia.JPG'
                }
            }
        },
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Serena'
                },
                'created_time': '18 Aprile 2016',
                'text': 'Il piu bel giorno della mia vita, grazie Antonio #nozze #matrimonio #ilpiubelgiornodellamiavita',
            },
            'location': {
                'name': 'Arco'
            },
            'likes': {
                'count': '48'
            },
            'images': {
                'standard_resolution': {
                    'url': 'http://img.tgcom24.mediaset.it/binary/istockphoto/52.$plit/C_4_articolo_2160799_upiImagepp.jpg'
                }
            }
        },
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Marco'
                },
                'created_time': '15 Aprile 2016',
                'text': 'Bellissima giornata, bellissime nozze, grazie Luisa #matrimonio #nozze #amore',
            },
            'location': {
                'name': 'Bassano'
            },
            'likes': {
                'count': '13'
            },
            'images': {
                'standard_resolution': {
                    'url': 'http://www.donnamoderna.com/var/ezflow_site/storage/images/media/images/matrimonio/proposte-di-nozze-vip/matrimonio-cruise-holmes/6389641-2-ita-IT/Matrimonio-Cruise-Holmes_s_dm11_tq.jpg'
                }
            }
        },
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Annalisa'
                },
                'created_time': '8 Aprile 2016',
                'text': 'Ho detto di si!!! Grazie Fabrizio !! #silovoglio #matrimonio',
            },
            'location': {
                'name': 'Pinzolo'
            },
            'likes': {
                'count': '53'
            },
            'images': {
                'standard_resolution': {
                    'url': 'http://i.huffpost.com/gen/2408326/thumbs/o-MATRIMONIO-570.jpg?1'
                }
            }
        },
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Sergio'
                },
                'created_time': '6 April 2016',
                'text': 'Noi due insieme per sempre. Ti Amo #nozze #evviva #matrimonio',
            },
            'location': {
                'name': 'Lavis'
            },
            'likes': {
                'count': '19'
            },
            'images': {
                'standard_resolution': {
                    'url': 'http://www.matteogagliardoni.it/wp-content/uploads/2014/11/foto-reportage-matrimonio-Perugia.jpg'
                }
            }
        },
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Valeria'
                },
                'created_time': '28 Marzo 2016',
                'text': 'Grazie di tutto, la giornata piu bella della mia vita #matrimonio #nozze #giornostupendo',
            },
            'location': {
                'name': 'Cles'
            },
            'likes': {
                'count': '9'
            },
            'images': {
                'standard_resolution': {
                    'url': 'https://i.ytimg.com/vi/8s4UTHaFzJo/maxresdefault.jpg'
                }
            }
        },
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Franco'
                },
                'created_time': '28 Marzo 2016',
                'text': 'Per sempre insieme! #matrimonio #nozze',
            },
            'location': {
                'name': 'Pergine'
            },
            'likes': {
                'count': '27'
            },
            'images': {
                'standard_resolution': {
                    'url': 'http://www.fotografomatrimonio.torino.it/img/gallery/small/cerimonia-matrimonio.jpg'
                }
            }
        },




    ]

    return render(request, 'screencast/video.html', {'posts':dati})