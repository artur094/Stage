from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^fbphoto', hello.views.fbphotos),
    url(r'^fbprofile', hello.views.fb_profile),
    url(r'^fblogin', include('hello.urls')),
    url(r'^fbfriend', hello.views.fbfriends),
    url(r'^$', hello.views.fblogin),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
