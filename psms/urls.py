from django.conf import settings
from django.conf.urls.defaults import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect

from tastypie.api import Api

from events.api import EventResource
from locations.api import CategoryResource, LocationResource
from sources.api import SourceResource

admin.autodiscover()

v01_api = Api(api_name='v1.0')
v01_api.register(EventResource())
v01_api.register(CategoryResource())
v01_api.register(LocationResource())
v01_api.register(SourceResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1.0/locations/locations.kml$', 'locations.views.kml', name='locations-kml'),
    url(r'^api/v1.0/primarysource/sitemap/$', 'sources.views.sitemap', name='sources-sitemap'),
    url(r'^api/v1.0/primarysource/csv/$', 'sources.views.export', name='sources-export'),
    url(r'^api/', include(v01_api.urls)),
    url(r'^mw/$', 'sources.views.links', name='sources-links'),
    url(r'^$', lambda x: HttpResponseRedirect('/mw/')),
]
# serve /media/ in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
