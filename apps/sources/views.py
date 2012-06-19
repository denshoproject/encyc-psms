import json
import logging

import requests

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from sources.models import Source


logger = logging.getLogger(__name__)


def app_context(request):
    """Context processor that handles variables used in many views.
    """
    context = {
        'request': request,
        'JQUERY_VERSION': settings.JQUERY_VERSION,
    }
    return context


@require_http_methods(['GET',])
def links(request, template_name='sources/links.html'):
    headwords = []
    headword_sources_tmp = {}
    headword_sources = []
    bad_headword_sources = []
    # get list of headwords
    args = '?action=query&list=categorymembers&cmtitle=Category:Pages_Needing_Primary_Sources&cmlimit=500&format=json'
    url = '%s%s' % (settings.EDITORS_MEDIAWIKI_API, args)
    if settings.EDITORS_MEDIAWIKI_USER and settings.EDITORS_MEDIAWIKI_PASS:
        r = requests.get(url, (settings.EDITORS_MEDIAWIKI_USER, settings.EDITORS_MEDIAWIKI_PASS))
    else:
        r = requests.get(url)
    if r.status_code != 200:
        assert False
    data = json.loads(r.text)
    for member in data['query']['categorymembers']:
        headwords.append(member['title'])
        headword_sources_tmp[member['title']] = []
    # add sources
    for source in Source.objects.all():
        if source.headword in headwords:
            l = headword_sources_tmp[source.headword]
            l.append(source)
        else:
            bad_headword_sources.append(source)
    # package
    for headword in headwords:
        headword_sources.append( {'headword':headword, 'sources':headword_sources_tmp[headword]} )
    return render_to_response(
        template_name, 
        {'headwords':headwords,
         'headword_sources':headword_sources,
         'bad_headword_sources':bad_headword_sources,
         'wiki_url':settings.EDITORS_MEDIAWIKI_URL,},
        context_instance=RequestContext(request, processors=[app_context])
    )

@require_http_methods(['GET',])
def sitemap(request, template_name='sources/links.html'):
    """Returns just enough data for Front to generate a sitemap.xml
    """
    sources = {'objects':[],}
    for source in Source.objects.filter(published=True):
        s = {'encyclopedia_id': source.encyclopedia_id,
             'modified': str(source.modified),
             'wikititle': source.wikititle(),}
        sources['objects'].append(s)
    return HttpResponse(json.dumps(sources), mimetype='application/json')
