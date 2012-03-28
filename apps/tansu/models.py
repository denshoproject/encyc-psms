from django.db import models

from core.models import BaseModel



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

    def filename(self):
        return self.image.name.replace(IMAGEFILE_PATH,'')
