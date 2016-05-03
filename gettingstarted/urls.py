from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views_instagram
import hello.views_stage
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #url(r'^instagram/', include('hello.urls_instagram')),
    url(r'^mat/',include('hello.urls_matrimoni')),
    url(r'^', include('hello.urls_stage')),
    #url(r'^admin/', include(admin.site.urls)),
]
