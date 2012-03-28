from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from tansu.models import ImageFile


@require_http_methods(['GET',])
def index(request, template_name='tansu/index.html'):
    imagefiles = ImageFile.objects.all()
    return render_to_response(
        template_name, 
        {'imagefiles': imagefiles,},
        context_instance=RequestContext(request)
    )

@require_http_methods(['GET',])
def detail(request, filename, template_name='tansu/detail.html'):
    imagefile = get_object_or_404(ImageFile, image='tansu/%s' % filename)
    return render_to_response(
        template_name, 
        {'imagefile': imagefile,},
        context_instance=RequestContext(request)
    )
