from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect

from tastypie.api import Api

from locations.api import LocationResource
from sources.api import SourceResource
from tansu.api import EntityResource
from tansu.api import AudioFileResource, DocumentFileResource, ImageFileResource, VideoFileResource

admin.autodiscover()

v01_api = Api(api_name='v0.1')
v01_api.register(LocationResource())
v01_api.register(SourceResource())
v01_api.register(EntityResource())
v01_api.register(AudioFileResource())
v01_api.register(DocumentFileResource())
v01_api.register(ImageFileResource())
v01_api.register(VideoFileResource())

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v0.1/primarysource/sitemap/$', 'sources.views.sitemap', name='sources-sitemap'),
    url(r'^api/', include(v01_api.urls)),
    url(r'^tansu/', include('tansu.urls')),
    url(r'^mw/$', 'sources.views.links', name='sources-links'),
    url(r'^$', lambda x: HttpResponseRedirect('/mw/')),
)
# serve /media/ in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
