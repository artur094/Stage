from django.conf.urls import url

from . import views_facebook

urlpatterns = [
    url(r'^fbphoto', views_facebook.fbphotos),
    url(r'^fbprofile', views_facebook.fb_profile),
    url(r'^fblogin', views_facebook.fblogin),
    url(r'^fbfriend', views_facebook.fbfriends),
    url(r'^fbposts', views_facebook.fbposts),
    url(r'^$', views_facebook.fblogin),
]
