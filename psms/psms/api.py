import logging
logger = logging.getLogger(__name__)

from django.conf.urls import url

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from events.timeline import all_events
from locations import facilities
from sources.models import Source


@api_view(['GET'])
def index(request, format=None):
    """OpenAPI/Swagger: /api/swagger/
    """
    data = {
        'sources': reverse('api-sources', request=request),
        'events': reverse('api-events', request=request),
        'categories': reverse('api-categories', request=request),
        'locations': reverse('api-locations', request=request),
    }
    return Response(data)

@api_view(['GET'])
def sources(request, format=None):
    """Source images used in the Encyclopedia.
    
    JSON-formatted list of the entire set of primary sources.
    """
    return Response(
        Source.sources()
    )

@api_view(['GET'])
def events(request, format=None):
    """Timeline of the Japanese American story during World War II.
    
    JSON-formatted list of events.
    """
    return Response({
        'objects': all_events()
    })

@api_view(['GET'])
def categories(request, format=None):
    """Categories of JA confinement facilities used during World War II.
    
    JSON-formatted list of the entire set of facility types.
    Used to display subsets of the master list of locations.
    """
    return Response(
        facilities.categories()
    )

@api_view(['GET'])
def locations(request, format=None):
    """Locations of facilities used to confine Japanese Americans in World War II.
    
    JSON-formatted list of the entire set of facilities.
    """
    return Response({
        'objects': facilities.all_facilities()
    })
