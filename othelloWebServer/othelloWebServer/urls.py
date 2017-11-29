from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'othelloWebServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^othello/', include('othello.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
