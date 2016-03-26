from django.shortcuts import render
from facebook import *
from models import *
from django.db.models import Q
from django.http import HttpResponse
from flask import g, render_template, redirect, request, session
from lxml import html
import requests
from splinter import Browser


def matrimoni(request):
    trento_mat_starter = 'http://webapps.comune.trento.it/pretorioMatrimonio/ArkAccesso.do'
    trento_mat = 'http://webapps.comune.trento.it/pretorioMatrimonio/menuContext.do'

    print_str = ""

    browser = Browser('django')
    # Visit URL
    url = "http://webapps.comune.trento.it/pretorioMatrimonio/ArkAccesso.do"
    browser.visit(url)

    if browser.is_text_present("HTTP Status 500"):
        return HttpResponse("Error")

    link = browser.find_by_text('Visualizza Pubblicazioni di Matrimonio')
    # Interact with elements
    link.click()

    atti = browser.find_by_xpath("//tr[@class='td-celladark' or @class='td-cellalight']/td[3]")

    print "Number of atti: ",len(atti)
    for atto in atti:
        lui = ""
        lei = ""
        #print atto.text
        #print "Inizio a dividere le stringhe di atto 1"
        stringhe = atto.value.split(" ")
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
        print_str += "Sposo: "+lui
        print_str += "Sposa: "+lei
        print_str += "\n"

    print_str += "\nThe End"
    return HttpResponse(print_str)