from django.conf.urls.defaults import *

from tansu import views

urlpatterns = patterns(
    '',
    url(r'^(?P<filename>[a-zA-Z0-9 _.-]+)/$', views.detail, name='tansu-detail'),
    url(r'^$', views.index, name='tansu-index'),
)
