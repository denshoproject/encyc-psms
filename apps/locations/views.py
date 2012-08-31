from django.conf import settings
from django.http import HttpResponse

from locations import facilities as fac

def kml(request):
    return HttpResponse(fac.kml(), content_type="text/xml")
