from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signin$', views.world_view, name='signin'),
    url(r'^signup$', views.world_view, name='signup'),
    url(r'^myworld$', views.world_view, name='myworld'),
    url(r'', views.home_view, name='home')
]