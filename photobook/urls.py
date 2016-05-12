from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import lifeshare.views_instagram
import lifeshare.views_stage
# Examples:
# url(r'^$', 'photobook.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #url(r'^instagram/', include('lifeshare.urls_instagram')),
    #url(r'^mat/',include('lifeshare.urls_matrimoni')),
    url(r'^', include('lifeshare.urls_stage')),
    #url(r'^admin/', include(admin.site.urls)),
]
