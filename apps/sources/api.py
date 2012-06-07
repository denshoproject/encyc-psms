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
            'encyclopedia_id': ('exact','in',),
            }
    
    def dehydrate_original(self, bundle):
        if bundle.obj.original and hasattr(bundle.obj.original, 'url'):
            return bundle.obj.original.url
        return ''
    
    def dehydrate_display(self, bundle):
        if bundle.obj.display and hasattr(bundle.obj.display, 'url'):
            return bundle.obj.display.url
        return ''
    
    def dehydrate(self, bundle):
        # include small and large thumbnails
        thumbnail_sm = bundle.obj.thumbnail_sm()
        thumbnail_lg = bundle.obj.thumbnail_lg()
        if thumbnail_sm and hasattr(thumbnail_sm, 'url'):
            bundle.data['thumbnail_sm'] = bundle.obj.thumbnail_sm().url
        if thumbnail_lg and hasattr(thumbnail_lg, 'url'):
            bundle.data['thumbnail_lg'] = bundle.obj.thumbnail_lg().url
        return bundle
