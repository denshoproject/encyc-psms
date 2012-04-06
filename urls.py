from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

from tastypie.api import Api

from tansu.api import ImageFileResource

admin.autodiscover()

v01_api = Api(api_name='v0.1')
v01_api.register(ImageFileResource())

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v01_api.urls)),
    url(r'^tansu/', include('tansu.urls')),
    url(r'^$', lambda x: HttpResponseRedirect('/tansu/')),
)
