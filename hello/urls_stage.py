from django.conf.urls import url

from . import views_stage

urlpatterns = [
    url(r'^$', views_stage.matrimoni),
    url(r'^profile', views_stage.login),
]

