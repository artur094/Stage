from django.conf.urls import url

from . import instagram_views

urlpatterns = [
    url(r'^$', instagram_views.login),
    url(r'^profile', instagram_views.profile),
    url(r'^follows', instagram_views.follows),
    url(r'^followed', instagram_views.followedby),
]