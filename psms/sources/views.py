from datetime import datetime
import json
import logging
logger = logging.getLogger(__name__)

import requests
import unicodecsv

from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from sources.models import Source


def app_context(request):
    """Context processor that handles variables used in many views.
    """
    context = {
        'request': request,
        'JQUERY_VERSION': settings.JQUERY_VERSION,
    }
    return context


def index(request, template_name='sources/index.html'):
    return render(request, template_name, {})

@require_http_methods(['GET',])
@cache_page(settings.CACHE_TIMEOUT)
def export(request):
    """Returns all sources as a CSV spreadsheet.
    """
    logging.debug('------------------------------------------------------------------------')
    filename = 'primarysources-%s.csv' % datetime.now().strftime('%Y%m%d-%H%M')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = unicodecsv.writer(response, encoding='utf-8', dialect='excel')
    # fieldnames in first row
    fieldnames = []
    for field in Source._meta.fields:
        fieldnames.append(field.name)
    writer.writerow(fieldnames)
    # data rows
    for source in Source.objects.all():
        values = []
        for field in fieldnames:
            values.append( getattr(source, field) )
        writer.writerow(values)
    # done
    return response

@require_http_methods(['GET',])
@cache_page(settings.CACHE_TIMEOUT)
def sitemap(request, template_name='sources/links.html'):
    """Returns just enough data for Front to generate a sitemap.xml
    """
    sources = {'objects':[],}
    for source in Source.objects.filter(published=True):
        s = {'encyclopedia_id': source.encyclopedia_id,
             'modified': str(source.modified),
             'wikititle': source.wikititle(),}
        sources['objects'].append(s)
    return JsonResponse(sources)
