import logging

from django.conf import settings
from django.db import models

from core.models import BaseModel

logger = logging.getLogger(__name__)


"""
Headword
varchar Title of MediaWiki page that the source appears on.

Densho ID
varchar Densho UID code.

Encyclopedia ID
varchar ???

Caption
text Textual description of the media object in context of the encyclopedia page.
This is different from the description field in the context of the Digital Repository.

Courtesy of
text Rights information.

Institution ID
varchar Keyword or short textual description of institution. NOT A PRIMARY KEY!

Collection Name
varchar Name of collection
"""

MEDIA_PATH = 'sources/'

def get_object_upload_path(file_object, filename):
    """Callable FileField.upload_to - see model field reference.
    
    Files for each id are kept in a directory named after the id.
    
    >>> img = Source()
    >>> img.id = 1
    >>> get_item_files_path(img, 'img.jpg')
    'sources/1/img.jpg'
    >>> img.id = 56
    >>> get_item_files_path(img, 'img.jpg')
    'sources/56/img.jpg'
    >>> img.id = 2501
    >>> get_item_files_path(img, 'img.jpg')
    'sources/2501/img.jpg'
    """
    return '%s%s/%s' % (MEDIA_PATH, str(file_object.id), filename)


class Source(BaseModel):
    #created
    #modified
    densho_id = models.CharField(max_length=255)
    headword = models.CharField(max_length=255)
    encyclopedia_id = models.CharField(max_length=255, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    courtesy = models.TextField(blank=True, null=True)
    institution_id = models.CharField(max_length=255, blank=True, null=True)
    collection_name = models.CharField(max_length=255, blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)
    creative_commons = models.BooleanField(default=False)
    media = models.FileField(upload_to=get_object_upload_path, blank=True, null=True)
    display = models.ImageField(upload_to=get_object_upload_path, blank=True, null=True)
    MEDIA_FORMATS = (
        ('image', 'photo'),
        ('document', 'document'),
        ('video', 'VH'),
        )
    media_format = models.CharField(max_length=32, choices=MEDIA_FORMATS, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Primary Source'
        verbose_name_plural = 'Primary Sources'
    
    def __unicode__(self):
        return '(%s) %s' % (self.densho_id, self.caption)
    
    @models.permalink
    def get_absolute_url(self):
        return ('sources-source-detail', (), {'uid': self.uid })
