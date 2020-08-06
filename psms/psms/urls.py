from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path
admin.autodiscover()

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from sources.views import index, export, sitemap
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
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('rest_framework.urls')),
    #path('api/swagger<slug:format>\.json|\.yaml)',
    #     schema_view.without_ui(cache_timeout=0), name='schema-json'
    #),
    path('api/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'
    ),
    path('api/redoc/',
        schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'
    ),
    
    path('api/2.0/primarysource/sitemap/', sitemap, name='sources-sitemap'),
    path('api/2.0/primarysource/csv/', export, name='sources-export'),
    
    path('api/2.0/sources/source/<slug:densho_id>/',
        api.source, name='api-source'
    ),
    path('api/2.0/sources/<slug:encyclopedia_ids>/',
        api.sources, name='api-sources'
    ),
    path('api/2.0/sources/',    api.sources,    name='api-sources'),
    path('api/2.0/',            api.index,      name='api-index'),
    path('api/1.0/',            api.index,      name='api-index'),
    path('api/',                api.index,      name='api-index'),
    
    path('', index, name='sources-index'),
]
# serve /media/ in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
