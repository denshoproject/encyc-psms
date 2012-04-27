import logging

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from tansu.models import Entity, AudioFile, DocumentFile, ImageFile, VideoFile


logger = logging.getLogger(__name__)


def app_context(request):
    """Context processor that handles variables used in many views.
    """
    context = {
        'request': request,
    }
    return context


@require_http_methods(['GET',])
def index(request, template_name='tansu/index.html'):
    entities = Entity.objects.all()
    return render_to_response(
        template_name, 
        {'entities': entities,},
        context_instance=RequestContext(request, processors=[app_context])
    )

@require_http_methods(['GET',])
def entity_detail(request, uid, template_name='tansu/entity-detail.html'):
    entity = get_object_or_404(Entity, uid=uid)
    return render_to_response(
        template_name, 
        {'entity': entity,},
        context_instance=RequestContext(request, processors=[app_context])
    )

@require_http_methods(['GET',])
def instance_detail(request, uid, model, object_id, template_name='tansu/instance-detail.html'):
    entity = get_object_or_404(Entity, uid=uid)
    instance = entity.instance(model, object_id)
    if not instance:
        raise Http404
    return render_to_response(
        template_name, 
        {'entity': entity,
         'instance':instance,},
        context_instance=RequestContext(request, processors=[app_context])
    )
