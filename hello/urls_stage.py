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
    url(r'^privacy', views_stage.privacy),

    # Saving and Display
    url(r'^save', views_stage.save_magazine),
    url(r'^magazine', views_stage.magazine),

    # List Previous Magazine
    url(r'^previous', views_stage.previous),

    # Settings
    url(r'^settings', views_stage.settings),
    #url(r'^list_magazine', views_stage.list_magazine),

    # Testing
    #url(r'^video', views_stage.video),
    url(r'^test',views_stage.test)
]

