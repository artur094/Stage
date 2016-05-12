from django.conf.urls import url

from . import views_facebook

urlpatterns = [
    url(r'^$', views_facebook.fblogin),
]