from django.conf.urls import url

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from events.timeline import all_events


@api_view(['GET'])
def events(request, format=None):
    """EVENTS DESCRIPTION GOES HERE
    """
    return Response({
        'objects': all_events()
    })
