from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from tansu.models import ImageFile

class ImageFileResource(ModelResource):
    class Meta:
        queryset = ImageFile.objects.all()
        resource_name = 'imagefile'
        #excludes = []
        allowed_methods = ['get']
        filtering = {'uri':ALL,}
