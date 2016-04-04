from django.conf.urls import url

from . import views_stage

urlpatterns = [
    url(r'^$', views_stage.matrimoni),
    url(r'^test', views_stage.test),
    url(r'^login', views_stage.login),
    url(r'^profile', views_stage.profile),
]

