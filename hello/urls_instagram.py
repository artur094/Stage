from django.conf.urls import url

from . import views_instagram

urlpatterns = [
    url(r'^$', views_instagram.login),
    url(r'^token', views_instagram.token),
    url(r'^profile', views_instagram.profile),
    url(r'^search', views_instagram.search),
    url(r'^hashtags', views_instagram.hashtags),

    #da cancellare
    url(r'^follows', views_instagram.follows),
    url(r'^followed', views_instagram.followedby),
]