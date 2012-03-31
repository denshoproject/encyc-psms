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

    @models.permalink
    def get_absolute_url(self):
        return ('tansu-detail', (), {'filename': self.filename() })
    
    def __unicode__(self):
        return self.image.name

    def save(self):
        """Uploads image to mediawiki, or updates description for existing file.
        """
        super(ImageFile, self).save()
        if self.image:
            page_name = 'File:%s' % self.image.name.capitalize()
            response = None
            if not wiki.exists(page_name):
                assert False
                response = wiki.upload_file(abspath, self.description)
            else:
                response = wiki.update_file(page_name, self.description)
            assert False
    
    def delete(self):
        """Deletes image from mediawiki.
        """
        super(ImageFile, self).delete()
        if self.image:
            page_name = 'File:%s' % self.image.name.capitalize()
            response = wiki.update_file(page_name, self.description)
            assert False

    def filename(self):
        return self.image.name.replace(IMAGEFILE_PATH,'')
