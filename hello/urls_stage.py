from django.conf.urls import url

from . import views_stage

urlpatterns = [
    url(r'^$', views_stage.index),
    url(r'^testing', views_stage.test_everything),
    url(r'^matrimoni', views_stage.matrimoni),
    url(r'^test_prof', views_stage.test),
    url(r'^test_search', views_stage.test_search),
    url(r'^login', views_stage.login),
    url(r'^token', views_stage.token),
    url(r'^profile', views_stage.insta_posts),

    url(r'^video', views_stage.video),
]

