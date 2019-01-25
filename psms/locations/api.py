from django.conf.urls import url

from rest_framework.decorators import api_view
from rest_framework.response import Response

from locations import facilities


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
