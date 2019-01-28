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
    """Swagger UI: /api/swagger/
    """
    data = {
        'events': reverse('api-events', request=request),
        'categories': reverse('api-categories', request=request),
        'locations': reverse('api-locations', request=request),
    }
    return Response(data)

@api_view(['GET'])
def sources(request, format=None):
    """PRIMARYSOURCES DESCRIPTION GOES HERE
    """
    return Response({
    })

@api_view(['GET'])
def events(request, format=None):
    """EVENTS DESCRIPTION GOES HERE
    """
    return Response({
        'objects': all_events()
    })

@api_view(['GET'])
def categories(request, format=None):
    """CATEGORIES DESCRIPTION GOES HERE
    """
    return Response(
        facilities.categories()
    )

@api_view(['GET'])
def locations(request, format=None):
    """LOCATIONS DESCRIPTION GOES HERE
    """
    return Response({
        'objects': facilities.all_facilities()
    })
