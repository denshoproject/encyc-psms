from django.conf.urls.defaults import *

from tansu import views

urlpatterns = patterns(
    '',
    url(r'^(?P<model>\w+)/(?P<id>\d+)/$', views.instance_detail, name='tansu-instance-detail'),
    url(r'^(?P<uid>[\w .-]+)/$', views.entity_detail, name='tansu-entity-detail'),
    url(r'^$', views.index, name='tansu-index'),
)
