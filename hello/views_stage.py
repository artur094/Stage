from django.shortcuts import render
from facebook import *
from models import *
from django.db.models import Q
from django.http import HttpResponse
from flask import g, render_template, redirect, request, session
from lxml import html
import requests


def matrimoni(request):
    trento_mat_starter = 'http://webapps.comune.trento.it/pretorioMatrimonio/ArkAccesso.do'
    trento_mat = 'http://webapps.comune.trento.it/pretorioMatrimonio/menuContext.do'

    tmp_page = requests.get(trento_mat_starter)
    page = requests.get(trento_mat)
    #tree = html.fromstring(tmp_page.content)

    return HttpResponse(page.content)
    #return render(request, 'index.html')