from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^myworld$', views.world_view, name='myworld'),
    url(r'', views.home_view, name='home')
]