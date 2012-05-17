from django.conf.urls.defaults import url

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from sources.models import Source


class SourceResource(ModelResource):
    class Meta:
        queryset = Source.objects.all()
        resource_name = 'primarysource'
        excludes = ['notes','update_display',]
        allowed_methods = ['get']
        filtering = {
            'densho_id':ALL,
            'encyclopedia_id': ('in',),
            }
