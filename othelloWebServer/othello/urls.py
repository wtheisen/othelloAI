from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$othello/index2.html', views.index2, name='index'),
    url(r'^test_post$', views.test_post, name='test_post'),
]
