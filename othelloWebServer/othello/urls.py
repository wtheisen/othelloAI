from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^index2$', views.index2, name='index'),
    url(r'^test_post$', views.test_post, name='test_post'),
    url(r'^$', views.main, name='main'),
    url(r'^update$', views.new_move, name='new_move'),
    url(r'^check$', views.check_valid_moves, name='check_move'),
    url(r'^stats$', views.get_global_stats, name='get_global_stats'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^winner$', views.post_game_stats, name="post_game_stats"),    
    url(r'^userinfo$', views.get_user_info, name="get_user_info"),    
    url(r'^userstats$', views.get_user_stats, name="get_user_stats"),    
    url(r'^logout$', views.post_logout, name="post_logout"),    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
