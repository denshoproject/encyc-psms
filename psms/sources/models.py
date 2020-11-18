from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)
import os

import unicodecsv

from django.conf import settings
from django.db import models
from django.template import loader

from sorl.thumbnail import get_thumbnail, delete as delete_thumbnail

from core.models import BaseModel
from sources import wiki

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

WIKI_IMG_LINK = "[[%s|right|200px]]\n"

MEDIA_FORMATS = (
    ('image', 'photo'),
    ('document', 'document'),
    ('video', 'VH'),
    )

THUMBNAIL_SM = 260
THUMBNAIL_LG = 700

ASPECT_RATIOS = (
    ('hd', 'HD'),
    ('sd', 'SD'),
    )

VALID_MEDIA = {
    'image':    ['orig:----:----:----',
                 '----:----:keyf:----',
                 'orig:----:keyf:----',
                 'orig:----:keyf:tran',
                 '----:----:keyf:tran',
                 ],
    'document': ['orig:----:----:----',
                 'orig:----:keyf:----',
                 'orig:----:keyf:tran',],
    'video':    ['orig:----:keyf:----',
                 'orig:----:keyf:tran',
                 '----:strm:keyf:----',
                 '----:strm:keyf:tran'],
    } #           |    |    |    |
#                 |    |    |    + transcript
#                 |    |    + keyframe
#                 |    + streaming url
#                 + original file


def get_object_upload_path(file_object, filename):
    """Callable FileField.upload_to - see model field reference.
    
    Files for each id are kept in a directory named after the id.
    
    >>> img = Source()
    >>> img.id = 1
    >>> get_object_upload_path(img, 'img.jpg')
    'sources/1/1/img.jpg'
    >>> img.id = 56
    >>> get_object_upload_path(img, 'img.jpg')
    'sources/5/56/img.jpg'
    >>> img.id = 2501
    >>> get_object_upload_path(img, 'img.jpg')
    'sources/2/2501/img.jpg'
    """
    idstr = str(file_object.id)
    return '%s%s/%s/%s' % (MEDIA_PATH, idstr[0], idstr, filename)

class Source(BaseModel):
    #created
    #modified
    published = models.BooleanField(default=False)
    densho_id = models.CharField(max_length=255, help_text="Valid DDR object ID")
    headword = models.CharField(max_length=255, help_text="Article title in editors' wiki")
    encyclopedia_id = models.CharField(max_length=255, unique=True, help_text="Valid DDR or Densho ID (must be unique)")
    caption = models.TextField(blank=True, null=True,
        help_text='Contents of this field will be visible on the article page, ' \
                  'in lightboxes, and on the Primary Source detail page.')
    caption_extended = models.TextField('Caption (Extended)', blank=True, null=True,
        help_text='Contents of this field will only be visible on the Primary Source detail page.')
    courtesy = models.TextField(blank=True, null=True)
    institution_id = models.CharField(max_length=255, blank=True, null=True)
    collection_name = models.CharField(max_length=255, blank=True, null=True)
    external_url = models.URLField(blank=True, null=True,)
    creative_commons = models.BooleanField(default=False)
    original = models.FileField('Original', upload_to=get_object_upload_path, blank=True, null=True,
        help_text='Full-size file from which thumbnails, keyframes, etc are derived')
    original_size = models.IntegerField(blank=True, null=True,)
    streaming_url = models.CharField('Streaming URL', max_length=100, blank=True, null=True,
        help_text='URL for streaming media (video, audio). Must be a full URL, including domain name.')
    transcript = models.FileField(upload_to=get_object_upload_path, blank=True, null=True)
    display = models.ImageField(upload_to=get_object_upload_path, blank=True, null=True,
        help_text='Image file used in lists and other interstitial pages')
    update_display = models.BooleanField('Refresh display', default=False,
        help_text="Refresh copy of display file in MediaWiki (click this if the image in MediaWiki doesn't change.")
    media_format = models.CharField('Format', max_length=32, choices=MEDIA_FORMATS)
    aspect_ratio = models.CharField(max_length=32, choices=ASPECT_RATIOS, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Primary Source'
        verbose_name_plural = 'Primary Sources'
    
    def save(self):
        """Sync media with wiki.
        
        see: http://192.168.0.13/redmine/issues/58
        Uses Densho UID as filename (example: denshopd-i114-00001.jpg).
        File description (on MediaWiki) should include:
        - caption
        - courtesy fields
        - link to edit page in Django admin
        """
        logging.debug('save(%s)' % self)
        # pre
        update_display = self.update_display
        self.update_display = False
        try:
            self.original_size = self.original.size
        except FileNotFoundError:
            pass
        # save
        super(Source, self).save()
        # post
        self.thumbnail_sm()            # TODO: celery
        self.thumbnail_lg()            # TODO: celery
        self.wiki_sync(update_display) # TODO: celery
    
    def delete(self):
        """Removes media from wiki on deletion.
        """
        logging.debug('delete(%s)' % self)
        self.wiki_delete()
        if self.display:
            delete_thumbnail(self.display)
        if self.original:
            delete_thumbnail(self.original)
        super(Source, self).delete()
    
    def __unicode__(self):
        return '(%s %s) %s' % (self.id, self.densho_id, self.caption[:50])

    def dict(self):
        return {
            f: str(getattr(self, f))
            for f in [field.name for field in Source._meta.fields]
        }

    #@models.permalink
    def get_absolute_url(self, http_host=settings.EDITORS_MEDIAWIKI_URL):
        """Returns link to editors' MediaWiki page or streaming URL for this Densho UID
        
        >>> s0 = Source(encyclopedia_id='en-densho-i337-01', display='asdf.jpg')
        >>> s0.get_absolute_url(http_host='http://10.0.4.15:9000/mediawiki/index.php')
        'http://10.0.4.15:9000/mediawiki/index.php/File:en-densho-i337-01.jpg'
        >>> s1 = Source(streaming_url='http://youtu.be/vf9wHkkNGUU')
        >>> s1.get_absolute_url()
        'http://youtu.be/vf9wHkkNGUU'
        >>> s2 = Source(id=123)
        >>> s2.get_absolute_url()
        '/admin/sources/source/123/'
        >>> s3 = Source()
        >>> s3.get_absolute_url()
        '/admin/sources/source/'
        """
        if self.streaming_url:
            return self.streaming_url
        elif self.wikititle():
            return '/'.join([http_host, self.wikititle()])
        elif self.id:
            return '/admin/sources/source/%s/' % self.id
        return '/admin/sources/source/'
    
    def admin_url(self, http_host=settings.SOURCES_HTTP_HOST):
        """Get a link to the admin interface.
        
        @param http_host IP address or domain name (for testing).
        
        >>> s0 = Source(id=123)
        >>> s0.admin_url(http_host='http://10.0.4.15:8001')
        'http://10.0.4.15:8001/admin/sources/source/123/'
        >>> s1 = Source()
        >>> s1.get_absolute_url()
        '/admin/sources/source/'
        """
        if self.id:
            return '%s/admin/sources/source/%s/' % (http_host, self.id)
        return '/admin/sources/source/'
    
    def is_valid(self):
        """Tells if record is well-formed according to its media type.
        """
        if self.media_format:
            keys = []
            if self.original:      keys.append('orig')
            else:                  keys.append('----')
            if self.streaming_url: keys.append('strm')
            else:                  keys.append('----')
            if self.display:       keys.append('keyf')
            else:                  keys.append('----')
            if self.transcript:    keys.append('tran')
            else:                  keys.append('----')
            keys = ':'.join(keys)
            if keys in VALID_MEDIA[self.media_format]:
                return True
        return False
    is_valid.short_description = 'Valid'
    is_valid.boolean = True
    
    def select_upload_file(self):
        """Display if present, media if not.
        
        In future this should do The Right Thing with non-image media.
        
        >>> s0 = Source(display='sources/01.jpg')
        >>> s0.select_upload_file()
        <ImageFieldFile: sources/01.jpg>
        >>> s1 = Source(original='sources/00.jpg')
        >>> s1.select_upload_file()
        <FieldFile: sources/00.jpg>
        >>> s2 = Source(original='sources/00.jpg', display='sources/01.jpg')
        >>> s2.select_upload_file()
        <ImageFieldFile: sources/01.jpg>
        """
        if self.display:
            return self.display
        elif self.original:
            return self.original
        return None

    def thumbnail_lg(self):
        if not hasattr(self, '_thumbnail_lg'):
            self._thumbnail_lg = None
            if   self.display:
                try:
                    self._thumbnail_lg = get_thumbnail(self.display, str(THUMBNAIL_LG))
                except:
                    logging.error('Source.thumbnail_lg display  %s' % self)
            elif self.original:
                try:
                    self._thumbnail_lg = get_thumbnail(self.original, str(THUMBNAIL_LG))
                except:
                    logging.error('Source.thumbnail_lg original %s' % self)
        return self._thumbnail_lg
    def thumbnail_sm(self):
        if not hasattr(self, '_thumbnail_sm'):
            self._thumbnail_sm = None
            if   self.display:
                try:
                    self._thumbnail_sm = get_thumbnail(self.display, str(THUMBNAIL_SM))
                except:
                    logging.error('Source.thumbnail_sm display  %s' % self)
            elif self.original:
                try:
                    self._thumbnail_sm = get_thumbnail(self.original, str(THUMBNAIL_SM))
                except:
                    logging.error('Source.thumbnail_sm original %s' % self)
        return self._thumbnail_sm

    def upload_filename(self):
        """Returns filename to be uploaded to wiki (ENCYCLOPEDIA_ID.DISPLAY_EXT)
        
        Upload a file that represents this entity, which is identified by its
        Encyclopedia ID.  Rename the file, keeping the file extension.
        
        >>> s0 = Source(encyclopedia_id='en-denshopd-1337-1', display='123.png')
        >>> s0.upload_filename()
        'en-denshopd-1337-1.png'
        >>> s1 = Source(encyclopedia_id='en-denshopd-1337-1', original='456.jpg')
        >>> s1.upload_filename()
        'en-denshopd-1337-1.jpg'
        >>> s2 = Source(encyclopedia_id='en-denshopd-1337-1', original='123.pdf', display='456.jpg')
        >>> s2.upload_filename()
        'en-denshopd-1337-1.jpg'
        >>> s3 = Source(encyclopedia_id='en-denshopd-1337-2')
        >>> s3.upload_filename()
        ''
        """
        if self.select_upload_file():
            return '%s%s' % (self.encyclopedia_id,
                             os.path.splitext(self.select_upload_file().name)[1])
        return ''
    
    def upload_filename_abspath(self, media_root=settings.MEDIA_ROOT):
        """Returns absolute path of upload filename; see upload_filename().
        
        >>> s0 = Source(encyclopedia_id='en-denshopd-1337-1', display='123.png')
        >>> s0.id = 987
        >>> s0.upload_filename_abspath()
        '/var/www/html/psms/media/sources/987/123.png'
        >>> s1 = Source(encyclopedia_id='en-denshopd-1337-1', display='123.png')
        >>> s1.upload_filename_abspath()
        ''
        """
        if self.id:
            partial = get_object_upload_path(self, self.select_upload_file().name)
            return '/'.join([media_root, partial]).replace('//', '/')
        return ''
    
    def wikititle(self):
        """Returns MediaWiki page name (DENSHOUID.DISPLAY_EXT)
        
        >>> s0 = Source(encyclopedia_id='en-denshopd-1337-1', display='123.png')
        >>> s0.wikititle()
        'File:en-denshopd-1337-1.png'
        >>> s1 = Source(encyclopedia_id='en-denshopd-1337-1', original='456.pdf')
        >>> s1.wikititle()
        'File:en-denshopd-1337-1.pdf'
        >>> s1 = Source(encyclopedia_id='en-denshopd-1337-1', original='123.pdf', display='456.jpg')
        >>> s1.wikititle()
        'File:en-denshopd-1337-1.jpg'
        >>> s2 = Source(encyclopedia_id='en-denshopd-1337-1')
        >>> s2.wikititle()
        ''
        """
        if self.select_upload_file():
            return 'File:%s' % self.upload_filename()
        return ''
    
    def wikitext(self, http_host=settings.SOURCES_HTTP_HOST):
        """Text of File:* page.
        
        File description (on MediaWiki) should include:
        - caption
        - caption_extended
        - courtesy fields
        - link to edit page in Django admin
        
        @param http_host IP address or domain name (for testing).
        """
        t = loader.get_template('sources/mediawiki-file-page.html')
        c = {'source': self}
        return t.render(c)
    
    def wiki_sync(self, update_display):
        """Decide whether to upload a new file or update existing info.
        """
        logging.debug('wiki_sync(%s)' % self)
        if not self.wikititle():
            return None
        # assemble the variables
        keys = []
        upload_file = self.select_upload_file()
        mw = wiki.MediaWiki()
        page_exists = mw.exists(self.wikititle())
        if page_exists:
            logging.debug('page exists')
            link_exists = self._wiki_link_exists(mw)
        else:
            link_exists = False
        if upload_file:    keys.append('file') # uploadable file exists
        else:              keys.append('----')
        if page_exists:    keys.append('page') # File:* page exists
        else:              keys.append('----')
        if update_display: keys.append('updt') # update_display checked
        else:              keys.append('----')
        if link_exists:    keys.append('link') # link present on page
        else:              keys.append('----')
        keys = ':'.join(keys)
        logging.debug('    keys: %s' % keys)
        # consult table, get names of functions to execute, and run them on self
        DECISION_TABLE = {
            #uploadable file exists
            #|    File:* page exists
            #|    |    update_display checked
            #|    |    |    link present on page
            #|    |    |    |
            'file:page:updt:link': ['upload','update',                ],
            'file:page:updt:----': ['upload','update','link',         ],
            'file:page:----:link': [         'update',                ],
            'file:page:----:----': [         'update','link',         ],
            'file:----:updt:link': ['upload','update',                ],
            'file:----:updt:----': ['upload','update','link',         ],
            'file:----:----:link': ['upload','update',                ],
            'file:----:----:----': ['upload','update','link',         ],
            '----:page:updt:link': [                         'delete',],
            '----:page:updt:----': [                         'delete',],
            '----:page:----:link': [                         'delete',],
            '----:page:----:----': [                         'delete',],
            '----:----:updt:link': [                                  ],
            '----:----:updt:----': [                                  ],
            '----:----:----:link': [                                  ],
            '----:----:----:----': [                                  ],
            }
        try:
            functions = DECISION_TABLE[keys]
        except:
            functions = []
        logging.debug('    functions: %s' % functions)
        for f in functions:
            function_name = '_wiki_%s' % f
            logging.debug(function_name)
            response = self.__getattribute__(function_name)(mw)
            logging.debug(response)
        # done!
        return response

    def _wiki_upload(self, mw):
        """Upload display file to wiki.
        
        symlink the wiki file, upload, rm symlink
        """
        logging.debug('_wiki_upload(%s)' % self)
        # upload initial file
        responses = []
        src = self.select_upload_file().path
        dest = os.sep.join([ os.path.dirname(src), self.upload_filename() ])
        logging.debug('        %s' % src)
        logging.debug('        > %s' % dest)
        symlinked = False
        if not os.path.exists(dest):
            os.symlink(src, dest)
            symlinked = True
            logging.debug('        symlinking...')
        response = mw.upload_file(dest, comment='Uploaded by PSMS/Tansu')
        responses.append(response)
        if symlinked:
            os.remove(dest)
            logging.debug('        symlinking DONE')
        # done
        logging.debug('    OK')
        return responses
    
    def _wiki_update(self, mw):
        """Just update the text of the File: page.
        """
        logging.debug('_wiki_update(%s)' % self)
        return mw.update_text(self.wikititle(), self.wikitext())
    
    def _wiki_linktext(self):
        return "[[%s|right|200px]]" % self.wikititle()
    
    def _wiki_link_exists(self, mw):
        return mw.link_exists(self.headword, self.wikititle())
    
    def _wiki_link(self, mw):
        logging.debug('Source._wiki_link')
        response = mw.prepend_text(self.headword, self._wiki_linktext())
        logging.debug('    OK')
        return response

    def wiki_delete(self, mw):
        logging.debug('_wiki_delete(%s)' % self)
        logging.debug('    NOT IMPLEMENTED')
    
    @staticmethod
    def sources(encyclopedia_ids=[]):
        """
        @param encyclopedia_ids: list Example: ['en-denshopd-i35-00428-1','en-denshopd-i67-00105-1']
        """
        if encyclopedia_ids:
            return [
                source.dict()
                for source in Source.objects.filter(
                    encyclopedia_id__in=encyclopedia_ids
                )
            ]
        return [source.dict() for source in Source.objects.all()]
    
    @staticmethod
    def source(densho_id):
        """
        @param densho_id: str
        """
        fieldnames = [
            field.name
            for field in Source._meta.fields
        ]
        source = Source.objects.get(densho_id=densho_id)
        o = OrderedDict()
        for f in fieldnames:
            o[f] = str(getattr(source, f))
        return o
    
    @staticmethod
    def export_csv(response):
        """
        @param response: django.http.HttpResponse
        @returns: django.http.HttpResponse
        """
        writer = unicodecsv.writer(response, encoding='utf-8', dialect='excel')
        # fieldnames in first row
        fieldnames = []
        for field in Source._meta.fields:
            fieldnames.append(field.name)
        writer.writerow(fieldnames)
        # data rows
        for source in Source.objects.all():
            values = []
            for field in fieldnames:
                values.append( getattr(source, field) )
            writer.writerow(values)
        return response
