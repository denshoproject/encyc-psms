from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
admin.autodiscover()

#from tastypie.api import Api
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

#from locations.views import kml as locations_kml
from sources.views import export, links, sitemap
from psms import api

#v01_api = Api(api_name='v1.0')
#v01_api.register(SourceResource())

API_BASE = '/api/2.0/'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/v1.0/locations/locations.kml$', locations_kml, name='locations-kml'),
    url(r'^api/v1.0/primarysource/sitemap/$', sitemap, name='sources-sitemap'),
    url(r'^api/v1.0/primarysource/csv/$', export, name='sources-export'),
    
    url(r'^api/v2.0/events',     api.events,     name='api-events'),
    url(r'^api/v2.0/categories', api.categories, name='api-categories'),
    url(r'^api/v2.0/locations',  api.locations,  name='api-locations'),
    url(r'^api/v2.0',            api.index,      name='api-index'),
    url(r'^api/v1.0',            api.index,      name='api-index'),
    url(r'^api',                 api.index,      name='api-index'),
    
    url(r'^mw/$', links, name='sources-links'),
    url(r'^$', lambda x: HttpResponseRedirect('/mw/')),
]
# serve /media/ in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
