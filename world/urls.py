from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signin$', views.sign_in_view, name='signin'),
    url(r'^signup$', views.sign_up_view, name='signup'),
    url(r'^myworld/(?P<user_id>[0-9]+)/$', views.world_view, name='myworld'),
    # url(r'', views.home_view, name='home')
]