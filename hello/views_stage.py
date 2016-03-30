from django.shortcuts import render
from facebook import *
from models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from flask import g, render_template, redirect, request, session
from lxml import html
import requests
from splinter import Browser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import my_class.instagram

hashtags = ['sposi', 'matrimonio', 'nozze', 'mariage', 'matrimoni']

client_id = '5afea7f15ea94a7cbf602fcdd54b0526'
client_secret = '1a861ce3f62547db9af64ac889af45d3'
redirect_uri = 'https://facebookalgorithm.herokuapp.com/profile'

self_users_url = 'https://api.instagram.com/v1/users/self/'


def matrimoni(request):
    vettore_sposi = []
    print_str = ""
    url = "http://webapps.comune.trento.it/pretorioMatrimonio/ArkAccesso.do"
    driver = webdriver.PhantomJS()
    #driver.set_window_size(1120, 550)
    driver.get(url)

    driver.find_element_by_xpath('//form[@id="menuContextForm"]//tr[2]/td/a').click()
    #driver.find_element_by_id("search_button_homepage").click()





    next = True
    while next:
        next = False

        atti = driver.find_elements_by_xpath("//tr[@class='td-celladark' or @class='td-cellalight']/td[3]")

        vettore_sposi.extend(sposi_of_list(atti))

        try:
            succ = driver.find_element_by_xpath("//a[@class='pagerSucc']")
            succ.click()
            next = True
        except NoSuchElementException:
            pass

    driver.quit()
    return render(request, 'index.html', {'sposi': vettore_sposi})


def sposi_of_list(atti):
    vettore_sposi = []
    for atto in atti:
        lui = ""
        lei = ""
        #print atto.text
        #print "Inizio a dividere le stringhe di atto 1"
        stringhe = atto.text.split(" ")
        #print "Finito la divisione dell'atto, ci sono: ",len(stringhe)

        for i in range(0, len(stringhe)):
            #print "Parola: ",stringhe[i]
            if stringhe[i] == "tra":
                j = i+1
                while(stringhe[j] != "nato"):
                    lui += stringhe[j]
                    lui += " "
                    j+=1
            if stringhe[i] == "e":
                j = i+1
                while(stringhe[j] != "nata"):
                    lei += stringhe[j]
                    lei +=" "
                    j+=1
        lui = lui[:len(lui)-1]
        lei = lei[:len(lei)-1]

        sposi = {'sposo':lui, 'sposa':lei}
        vettore_sposi.append(sposi)
    return vettore_sposi

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
    return render(request, 'social/instagram_profile.html', {'dati':inst.post_hashtag(hashtags[0], token)})


