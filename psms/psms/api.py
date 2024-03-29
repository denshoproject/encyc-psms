import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.views.decorators.cache import cache_page

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from events import timeline
from locations import facilities
from sources.models import Source


@api_view(['GET'])
def index(request, format=None):
    """OpenAPI/Swagger: /api/swagger/
    """
    data = {
        'sources': reverse('api-sources', request=request),
        'sources-sitemap': reverse('sources-sitemap', request=request),
        'sources-csv': reverse('sources-export', request=request),
        'events': reverse('api-events', request=request),
        'locations': reverse('api-locations', request=request),
    }
    return Response(data)

@api_view(['GET'])
@cache_page(settings.CACHE_TIMEOUT)
def sources(request, encyclopedia_ids=None, format=None):
    """Source images used in the Encyclopedia.
    
    JSON-formatted list of primary sources.
    If encyclopedia IDs <encyclopedia_ids> are specified, list sources
    for that particular page, otherwise the entire list with no pagination.
    
    @param : 'en-denshopd-i35-00428-1,en-denshopd-i67-00105-1'

    """
    if encyclopedia_ids:
        encyclopedia_ids = encyclopedia_ids.split(',')
    return Response(
        Source.sources(encyclopedia_ids)
    )

@api_view(['GET'])
def source(request, densho_id, format=None):
    """Source image used in the Encyclopedia.
    
    JSON-formatted record.
    """
    return Response(
        Source.source(densho_id)
    )

@api_view(['GET'])
def events(request, format=None):
    """Timeline of the Japanese American story during World War II.
    
    JSON-formatted list of events.
    """
    return Response({
        'objects': timeline.all_events()
    })

@api_view(['GET'])
def locations(request, format=None):
    """Locations of facilities used to confine Japanese Americans in World War II.
    
    JSON-formatted list of the entire set of facilities.
    """
    return Response({
        'objects': facilities.all_facilities()
    })
