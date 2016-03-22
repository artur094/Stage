from django.conf.urls import url

from . import views_instagram

urlpatterns = [
    url(r'^$', views_instagram.login),
    url(r'^profile', views_instagram.profile),
    url(r'^follows', views_instagram.follows),
    url(r'^followed', views_instagram.followedby),
]