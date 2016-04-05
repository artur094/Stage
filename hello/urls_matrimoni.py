from django.conf.urls import url

from . import views_matrimoni

urlpatterns = [
    url(r'^$', views_matrimoni.tutti_comuni),
    url(r'^arco', views_matrimoni.arco),
    url(r'^trento', views_matrimoni.trento),
    url(r'^rovereto', views_matrimoni.rovereto),
    url(r'^pergine', views_matrimoni.pergine),
    url(r'^pinzolo', views_matrimoni.pinzolo),
]

