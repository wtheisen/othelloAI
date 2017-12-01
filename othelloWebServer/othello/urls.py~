from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^index2$', views.index2, name='index'),
    url(r'^test_post$', views.test_post, name='test_post'),
    url(r'^$', views.main, name='main'),
    url(r'^update$', views.new_move, name='new_move'),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #        {'document_root', settings.STATIC_ROOT}
    #),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
