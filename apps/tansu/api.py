from django.conf.urls.defaults import url

from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from tansu.models import Entity, AudioFile, DocumentFile, ImageFile, VideoFile


class EntityResource(ModelResource):
    class Meta:
        queryset = Entity.objects.all()
        resource_name = 'entity'
        #excludes = []
        #allowed_methods = ['get']
        filtering = {'uri':ALL,}
        authentication = Authentication()
        authorization = DjangoAuthorization()
    
    def override_urls(self):
        """Use Densho UID in URL instead of entity.id.
        see django-tasypie docs "Tastypie Cookbook > Using Non-PK Data For Your URLs"
        """
        return [
            url(r"^(?P<resource_name>%s)/(?P<uid>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class AudioFileResource(ModelResource):
    class Meta:
        queryset = AudioFile.objects.all()
        resource_name = 'audio'
        #excludes = []
        allowed_methods = ['get']
        filtering = {'uri':ALL,}

class DocumentFileResource(ModelResource):
    class Meta:
        queryset = DocumentFile.objects.all()
        resource_name = 'document'
        #excludes = []
        allowed_methods = ['get']
        filtering = {'uri':ALL,}

class ImageFileResource(ModelResource):
    class Meta:
        queryset = ImageFile.objects.all()
        resource_name = 'image'
        #excludes = []
        allowed_methods = ['get']
        filtering = {'uri':ALL,}

class VideoFileResource(ModelResource):
    class Meta:
        queryset = VideoFile.objects.all()
        resource_name = 'image'
        #excludes = []
        allowed_methods = ['get']
        filtering = {'uri':ALL,}
