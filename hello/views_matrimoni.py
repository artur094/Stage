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

def tutti_comuni(request):

    mat = Matrimoni()
    mat.arco()
    mat.pergine()
    mat.trento()
    mat.rovereto()
    mat.pinzolo()

    sposi = Coppia.objects.all()

    return render(request, 'matrimoni.html', {'sposi': sposi})

def arco(request):
    mat = Matrimoni()
    mat.arco()
    sposi = Coppia.objects.filter(comune='Arco')
    return render(request, 'matrimoni.html', {'sposi': sposi})

def trento(request):
    mat = Matrimoni()
    mat.trento()
    sposi = Coppia.objects.filter(comune='Trento')
    return render(request, 'matrimoni.html', {'sposi': sposi})

def rovereto(request):
    mat = Matrimoni()
    mat.rovereto()
    sposi = Coppia.objects.filter(comune='Rovereto')
    return render(request, 'matrimoni.html', {'sposi': sposi})

def pergine(request):
    mat = Matrimoni()
    mat.pergine()
    sposi = Coppia.objects.filter(comune='Pergine')
    return render(request, 'matrimoni.html', {'sposi': sposi})

def pinzolo(request):
    mat = Matrimoni()
    mat.pinzolo()
    sposi = Coppia.objects.filter(comune='Pinzolo')
    return render(request, 'matrimoni.html', {'sposi': sposi})

