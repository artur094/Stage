from django.shortcuts import render
from django.db.models import Max
from facebook import *
from models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from flask import g, render_template, redirect, request, session
from lxml import html
import requests
import simplejson as json
from django.core import serializers
from splinter import Browser
from my_class.comune_matrimoni import Matrimoni
from my_class.instagram import Instagram
import models
from django.forms.models import model_to_dict


import my_class.instagram

hashtags = ['italy','sposi', 'matrimonio', 'nozze', 'mariage', 'matrimoni']

client_id = '84b7d3a446bc448da7e219f463db7ee9'
client_secret = '435767712dfe412d852262542d2fc05d'
redirect_uri = 'https://facebookalgorithm.herokuapp.com/token'
scope = 'public_content'
self_users_url = 'https://api.instagram.com/v1/users/self/'

list_customer_to_spy = [
    {
        'username':'utente_normale',
        'full_name':'User'
    }
]

def privacy(request):
    return render(request, 'privacy.html')

def index(request):
    return render(request, 'homepage.html')

def login(request):
    permissions = 'scope=basic+public_content'
    url = 'https://api.instagram.com/oauth/authorize/?client_id='+client_id+'&redirect_uri='+redirect_uri+'&response_type=code&'+permissions
    return HttpResponseRedirect(url)

def getToken(request):
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

    inst = Instagram()

    token = my_data.json()['access_token']
    me = inst.profile('self', token)

    request.session['token'] = token
    #request.session['me'] = me

    if User.objects.filter(id=me['id']).exists():
        request.session['me'] = User.objects.get(id=me['id'])
        return selection(request)

    u = User()
    u.id = me['id']
    u.username = me['username']
    u.img_src = me['profile_picture']

    request.session['me'] = u

    return signin(request)

#TODO check if the user is logged in instagram, and if he is, check if he has already signed up
def signin(request):
    return render(request, 'signin.html')


#TODO when the button is pressed, the page must go to the textbox which has the link
#TODO change weddings, holidays and relatives' post from hard coded to DB
#TODO change 'privacy' to 'magazine name' (or 'rsa location'?)
def selection(request):
    if 'token' not in request.session or 'me' not in request.session:
        return login(request)

    #Salvataggio dell'account
    if 'action' in request.GET:
        u = request.session['me']
        u.RSAname = request.GET['rsa_name']
        u.RSAlocation = request.GET['rsa_location']
        u.RSAmagazine = request.GET['magazine_name']
        u.save()
        request.session['me'] = u

        #now I save the default categories for the new user
        if not Category.objects.all().filter(name='weddings').exists():
            wedding = Category()
            wedding.rsa = u
            wedding.name = 'weddings'
            wedding.tags = 'wedding,marriage,engagement,proposal,matrimonio,proposta'
            wedding.instruction = 'Please select all the images that are related to wedding and engagement, avoiding advertising or impersonal pictures.'
            wedding.save()
        if not Category.objects.all().filter(name='holidays').exists():
            holidays = Category()
            holidays.rsa = u
            holidays.name = 'holidays'
            holidays.tags = 'holidays,trip,journey,travels,viaggio,vacanze'
            holidays.instruction = 'Please select all the pictures showing trips and travels, avoiding advertising or impersonal pictures.'
            holidays.save()
        if not Category.objects.all().filter(name="relatives' post").exists():
            relatives = Category()
            relatives.rsa = u
            relatives.name ="relatives' post"
            relatives.tags =''
            relatives.instruction = 'Please select all the pictures showing people and places, giving priority to well-visible faces and multiple subjects and avoiding advertising or impersonal pictures (e.g. quotes).'
            relatives.save()



    instagram = Instagram()
    token = request.session['token']
    me = request.session['me']

    list = []
    for category in Category.objects.all().filter(rsa=me):
        posts = []
        if category.name == "relatives' post":
            usernames = category.tags.split(',')
            for user in usernames:
                posts.extend(instagram.posts_from_username(user, token))
        else:
            tags = category.tags.split(',')
            results = instagram.search_hashtags_union(tags, token)
            posts.extend(results)

        list.append({
            'name': category.name,
            'data': posts,
            'instruction': category.instruction
        })


    '''
    #groups: wedding, holidays.. then what?

    wedding_hashtags = [
        'wedding', 'marriage', 'engagement', 'proposal','matrimonio','proposta'
    ]

    holidays_hashtags = [
        'holidays','trip','journey','travels','viaggio','vacanze'
    ]



    list_post_wedding = instagram.search_hashtags_union(wedding_hashtags, token)
    list_post_holidays = instagram.search_hashtags_union(holidays_hashtags, token)
    list_post_parents = []

    for customer in list_customer_to_spy:
        customer_profile = instagram.search_user(customer, token)
        if customer_profile is not None:
            customer_posts = instagram.posts(customer_profile['id'],token)
            list_post_parents.extend(customer_posts)

    #only for testing:
    list_post_wedding = dati = [
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
                    'url':'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/12940178_596391663844483_1231823169_n.jpg?ig_cache_key=MTIxODk5NDE5NjY5MTk0NjU3Ng%3D%3D.2.l'
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
                    'url': 'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/12940706_1575363102791750_1346733616_n.jpg?ig_cache_key=MTIxODk5MjU4NDAzMjM5MDE3MA%3D%3D.2'
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
    list_post_holidays = dati = [
        {
            'type': 'image',
            'caption': {
                'from': {
                    'username': 'Giorgio'
                },
                'created_time': '22 Aprile 2016',
                'text': 'Matrimonio con Lucia #nozze, #matrimonio, #nonsochehashtags',
            },
            'location': {
                'name': 'Trento'
            },
            'likes': {
                'count': '24'
            },
            'images': {
                'standard_resolution': {
                    'url': 'http://www.fotografi-matrimonio.com/padova-galleria-foto-fotoste-di-stefania-chiereghin/images/07-Foto-sposi-in-Chiesa-Santa-Giustina-Pernumia.JPG'
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
                    'url': 'http://www.fotosprint.info/public/content/0.jpg'
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
    list_post_parents = list_post_holidays
    #only for testing

    list = [
        {
            'name': 'weddings',
            'instruction': 'Please select all the images that are related to wedding and engagement, avoiding advertising or impersonal pictures.',
            'data': list_post_wedding
        },
        {
            'name': 'holidays',
            'instruction':'Please select all the pictures showing trips and travels, avoiding advertising or impersonal pictures.',
            'data': list_post_holidays
        },
        {
            'name':'relatives\' posts',
            'instruction':'Please select all the pictures showing people and places, giving priority to well-visible faces and multiple subjects and avoiding advertising or impersonal pictures (e.g. quotes).',
            'data': list_post_parents
        }

    ]
    '''

    return render(request, 'selection.html', {'data': list, 'user':me})

#TODO fix the presentation of the page
def magazine(request):
    instagram = Instagram()

    #if 'token' not in request.session:
    #    return index(request);

    if 'action' in request.POST:
        if 'token' not in request.session:
            return index(request)
        if 'me' not in request.session:
            return login(request)

        me = request.session['me']
        action = request.POST['action']

        if action == 'save':
            json_data = request.POST['data']
            data = json.loads(json_data)

            #list_images = request.POST.getlist('list_img[]')
            #type_magazine = request.POST['type']

            #Creo il magazine
            magazine = Magazine()
            magazine.user = me

            if Magazine.objects.all().filter(user=me).aggregate(Max('edition'))['edition__max'] is not None:
                magazine.edition = Magazine.objects.all().filter(user=me).aggregate(Max('edition'))['edition__max']+1
            else:
                magazine.edition = 1

            magazine.save()

            for type in data:
                if len(type['posts']) > 0 and Category.objects.all().filter(rsa=me).filter(name=type['type']).exists():
                    m_type = MagazineType()
                    m_type.category = Category.objects.all().filter(rsa=me).get(name=type['type'])
                    #m_type.type = type['type']
                    m_type.magazine = magazine
                    m_type.save()

                    for post in type['posts']:
                        image = Photo()
                        image.magazine_type = m_type
                        image.img_src = post['img_src']
                        image.id_creator = post['owner_id']
                        image.tags = post['tags']

                        creator = instagram.profile(image.id_creator, request.session['token'])

                        image.username_creator = creator['username']
                        image.img_src_creator = creator['profile_picture']

                        image.save()

            public_url_magazine = request.META['HTTP_HOST'] + '/magazine?id='+ magazine.id.__str__()
            return HttpResponse(public_url_magazine)

    #Se voglio vedere il magazine ID=X
    if 'id' in request.GET:
        id_magazine = request.GET['id']
        #Controllo se l'ID e' presente nel DB
        if not Magazine.objects.all().filter(id=id_magazine).exists():
            return HttpResponse('ERRORE!')

        magazine = Magazine.objects.get(id=id_magazine)


        if 'type' in request.GET:
            type = request.GET['type']
            if not Category.objects.all().filter(rsa=magazine.user).filter(name=type).exists():
                return HttpResponse('Error')

            category = Category.objects.all().filter(rsa=magazine.user).get(name=type)

            if MagazineType.objects.all().filter(magazine=magazine).filter(category=category).exists():
                magazine_type = MagazineType.objects.all().filter(magazine=magazine).get(type=type)
            else:
                return HttpResponse('Error')
        else:
            if MagazineType.objects.all().filter(magazine=magazine).exists():
                magazine_type = MagazineType.objects.all().filter(magazine=magazine)[0]
            else:
                return HttpResponse('Error')

        list_type_for_this_magazine = MagazineType.objects.all().filter(magazine=magazine).values('type').distinct()

        photos = Photo.objects.all().filter(magazine_type=magazine_type)

        for photo in photos:
            #reperisco username e profile_picture dell'owner della foto
            id_owner = photo.id_creator
            if 'token' in request.session:
                profile_owner = instagram.profile(id_owner, request.session['token'])
                photo.username_creator = profile_owner['username']
                photo.img_src_creator = profile_owner['profile_picture']

        return render(request, 'slideshow.html', {'list_type':list_type_for_this_magazine,'magazine':magazine,'magazine_type':magazine_type, 'user':magazine.user,'images':photos})
    #TODO Return a page which show all magazine with all RSA
    return HttpResponse('ERRORE!')


def settings(request):
    if 'me' not in request.session or 'token' not in request.session:
        return login(request)

    me = request.session['me']

    if 'action' in request.POST:
        data = json.loads(request.POST['data'])
        relatives = json.loads(request.POST['relatives'])



        #NON FUNZIONA PERCHE' MANCA L'ID
        '''
        Relative.objects.all().filter(rsa=me).delete()
        for relative in relatives['usernames']:
            r = Relative()
            r.rsa = me
            r.username = relative
            r.save()
            username+=relative+', '
        return HttpResponse(username)
        '''

        usernames = ''
        for relative in relatives['usernames']:
            usernames+=relative+','
        usernames = usernames[:len(usernames)-1]
        Category.objects.all().filter(rsa=me).filter(name="relatives' post").update(tags=usernames)


        for category in data:
            tags=''
            for tag in category['tags']:
                tags = tags + tag + ','
            tags = tags[:len(tags)-1]

            if Category.objects.all().filter(rsa=me).filter(name=category['name']).exists():
                Category.objects.all().filter(rsa=me).filter(name=category['name']).update(tags=tags)
            else:
                cat = Category()
                cat.rsa = me
                cat.tags = tags
                cat.name = category['name']
                cat.save()

        return HttpResponse('Settings saved')

    my_categories = Category.objects.all().filter(rsa=me).exclude(name="relatives' post")
    relatives =  Category.objects.all().filter(rsa=me).get(name="relatives' post")

    return render(request, 'settings.html', { 'user':me, 'categories': my_categories,'relatives':relatives})

def previous(request):
    return render(request, 'previous.html')

def test(request):
    return render(request, 'test.html')



















def list_magazine(request):
    url = request.META['HTTP_HOST'] + '/magazine?id='

    if 'action' in request.GET:
        if request.GET['type'] == 'user':
            user = User.objects.get(id=request.GET['id'])
            magazines = Magazine.objects.all().filter(user =user)
            user_serialized =model_to_dict(user)
            magazines_serialized = serializers.serialize('json', magazines)

            data = {
                'user':user_serialized,
                'magazines':magazines_serialized,
                'url': url
            }
            return JsonResponse(data)
        if request.GET['type'] == 'location':
            users = User.objects.all().filter(RSAlocation = request.GET['location'])

            data = {
                'url':url,
                'list_magazines':[]
            }

            for user in users:
                magazines = Magazine.objects.all().filter(user=user)

                data['list_magazines'].append({
                    'user':model_to_dict(user),
                    'magazines':serializers.serialize('json',magazines)
                })
            return JsonResponse(data)



    list_user = User.objects.all()
    list_location = User.objects.values('RSAlocation').distinct()
    list_rsa_name = User.objects.values('RSAname').distinct()
    list_magazine = Magazine.objects.all()



    return render(request, 'list_magazine.html', {'users': list_user,'magazines':list_magazine, 'locations':list_location, 'rsa_names':list_rsa_name, 'url':url})


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
                    'url':'https=2//scontent-mxp1-1=1cdninstagram=1com/t51=12885-15/s750x750/sh0=108/e35/12940706_1575363102791750_1346733616_n=1jpg?ig_cache_key=0MTIxODk5MjU4NDAzMjM5MDE3MA%3D%3D=12.0.2'
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
                    'url': 'http://www.fotosprint.info/public/content/0.jpg'
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