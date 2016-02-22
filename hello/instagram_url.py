from django.conf.urls import url

from . import instagram_views

urlpatterns = [
    url(r'^$', instagram_views.login),
    url(r'^profile', instagram_views.profile)
]