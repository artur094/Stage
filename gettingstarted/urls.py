from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import hello.instagram_views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^fbphoto', hello.views.fbphotos),
    url(r'^fbprofile', hello.views.fb_profile),
    url(r'^fblogin', hello.views.fblogin),
    url(r'^fbfriend', hello.views.fbfriends),
    url(r'^fbposts',hello.views.fbposts),
    url(r'^instagram/',include('hello.instagram_url')),
    url(r'^$', hello.views.fblogin),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
