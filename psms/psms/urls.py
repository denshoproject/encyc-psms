from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
admin.autodiscover()

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

#from locations.views import kml as locations_kml
from sources.views import export, links, sitemap
from psms import api

#v01_api = Api(api_name='v1.0')
#v01_api.register(SourceResource())

API_BASE = '/api/2.0/'

schema_view = get_schema_view(
   openapi.Info(
      title="Encyclopedia Primary Sources API",
      default_version='2.0',
      description="Back-end resources for the Densho Encyclopedia",
      terms_of_service="http://encyclopedia.densho.org/about/#tosprivacy",
      contact=openapi.Contact(email="info@densho.org"),
      license=openapi.License(name="TBD"),
   ),
   #validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    #path(r'^api/swagger(?P<format>\.json|\.yaml)',
    #     schema_view.without_ui(cache_timeout=0), name='schema-json'
    #),
    url(r'^api/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'
    ),
    url(r'^api/redoc/',
        schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'
    ),
    
    #url(r'^api/v1.0/locations/locations.kml$', locations_kml, name='locations-kml'),
    url(r'^api/2.0/primarysource/sitemap/$', sitemap, name='sources-sitemap'),
    url(r'^api/2.0/primarysource/csv/$', export, name='sources-export'),
    
    url(r'^api/2.0/sources/source/(?P<densho_id>[\w-]+)',
        api.source, name='api-source'
    ),
    url(r'^api/2.0/sources/(?P<encyclopedia_ids>[\w,-]+)',
        api.sources, name='api-sources'
    ),
    url(r'^api/2.0/sources',    api.sources,    name='api-sources'),
    url(r'^api/2.0/events',     api.events,     name='api-events'),
    url(r'^api/2.0/categories', api.categories, name='api-categories'),
    url(r'^api/2.0/locations',  api.locations,  name='api-locations'),
    url(r'^api/2.0',            api.index,      name='api-index'),
    url(r'^api/1.0',            api.index,      name='api-index'),
    url(r'^api',                api.index,      name='api-index'),
    
    url(r'^mw/$', links, name='sources-links'),
    url(r'^$', lambda x: HttpResponseRedirect('/mw/')),
]
# serve /media/ in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
