from django.conf.urls.defaults import *

from tansu import views

urlpatterns = patterns(
    '',
    url(r'^(?P<id>\d+)/$', views.detail, name='tansu-detail'),
    url(r'^$', views.index, name='tansu-index'),
)
