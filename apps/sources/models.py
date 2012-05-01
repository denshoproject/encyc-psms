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
