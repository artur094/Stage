from django.conf.urls import url

from . import views_stage

urlpatterns = [
    url(r'^$', views_stage.index),
    url(r'^matrimoni', views_stage.matrimoni),
    url(r'^test', views_stage.test),
    url(r'^login', views_stage.login),
    url(r'^token', views_stage.token),
    url(r'^profile', views_stage.insta_posts),
]

