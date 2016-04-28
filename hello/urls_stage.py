from django.conf.urls import url

from . import views_stage

urlpatterns = [
    # Instagram Login Pages
    url(r'^login', views_stage.login),
    url(r'^token', views_stage.getToken),

    # WebPages
    url(r'^$', views_stage.index),
    url(r'^signin', views_stage.signin),
    url(r'^selection', views_stage.selection),

    # Saving and Display
    url(r'^magazine', views_stage.magazine),
    url(r'^list_magazine', views_stage.list_magazine),

    # Testing
    url(r'^video', views_stage.video),
]

