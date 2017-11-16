from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index2$', views.index2, name='index'),
    url(r'^test_post$', views.test_post, name='test_post'),
    url(r'^$', views.main, name='main'),
    url(r'^update$', views.new_move, name='new_move')
]
