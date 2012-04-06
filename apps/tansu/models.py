import os

from django.conf import settings
from django.db import models

from core.models import BaseModel
from tansu import wiki


class MediaBase(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        abstract = True
    
    def mimetype(self):
        return 'unknown'



IMAGEFILE_PATH = 'tansu/'

class ImageFile(MediaBase):
    image = models.ImageField(upload_to=IMAGEFILE_PATH)
    size = models.IntegerField()
    uri = models.CharField(max_length=255)

    @models.permalink
    def get_absolute_url(self):
        return ('tansu-detail', (), {'id': self.id })
    
    def api_url(self):
        return '%s/imagefile/%s/' % (settings.TANSU_API, self.id)

    def api_filename_url(self):
        return '%s/imagefile/?uri=%s' % (settings.TANSU_API, self.uri)

    def edit_url(self):
        return '/admin/tansu/imagefile/%s/' % self.id
    
    def __unicode__(self):
        return self.image.name

    def save(self):
        """Uploads image to mediawiki, or updates description for existing file.
        """
        self.size = self.image.size
        self.uri = self.image.name
        super(ImageFile, self).save()
        if self.image:
            page_name = 'File:%s' % self.image.name.replace(IMAGEFILE_PATH,'')
            if not wiki.exists(page_name):
                path = '/'.join([settings.MEDIA_ROOT, self.image.name]).replace('//', '/')
                response = wiki.upload_file(path, self.description)
            else:
                response = wiki.update_file(page_name, self.description)
    
    def delete(self):
        """Deletes image from mediawiki.
        """
        super(ImageFile, self).delete()
        if self.image:
            page_name = 'File:%s' % self.image.name
            response = wiki.update_file(page_name, self.description)
            assert False

    def filename(self):
        return self.image.name.replace(IMAGEFILE_PATH,'')

    def media(self):
        return self.image
