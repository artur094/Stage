from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views_facebook
import hello.views_instagram
import hello.views_stage
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^facebook/', include('hello.urls_facebook')),
    url(r'^instagram/', include('hello.urls_instagram')),
    url(r'^$', hello.views_stage.matrimoni),
    url(r'^db', hello.views_facebook.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
