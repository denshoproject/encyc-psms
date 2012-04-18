"""

Entity
   |
+----------------
|Entity_Object
+----------------
| entity_id   (pk)
| instance_id (pk)
| model
| object_id
+----------------
   |
Audio / Document / Image / Video


"""
import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.db import models

from core.models import BaseModel
from tansu import wiki


MEDIA_PATH = 'tansu/'
FILE_OBJECT_TYPES = ['AudioFile', 'ImageFile', 'DocumentFile', 'VideoFile',]


class Entity(BaseModel):
    uid = models.CharField(max_length=255, unique=True,)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Intellectual Entity'
        verbose_name_plural = 'Intellectual Entities'
    
    def __unicode__(self):
        return '(%s) %s' % (self.uid, self.title)
    
    @models.permalink
    def get_absolute_url(self):
        return ('tansu-entity-detail', (), {'uid': self.uid })
    
    def edit_url(self):
        return '/admin/tansu/entity/%s/' % self.id
    
    def instances_all(self):
        """All instances including originals
        """
        instances = []
        for t in FILE_OBJECT_TYPES:
            object_type = ContentType.objects.get(app_label='tansu', model=t.lower())
            model_class = object_type.model_class()
            for instance in model_class.objects.filter(entity=self):
                instances.append(instance)
        return instances
    
    def instances(self):
        """Non-original instances
        """
        instances = []
        for instance in self.instances_all():
            if not instance.is_master:
                instances.append(instance)
        return instances
    
    def originals(self):
        originals = []
        for instance in self.instances_all():
            if instance.is_master:
                originals.append(instance)
        return originals


def get_object_upload_path(file_object, filename):
    """Callable FileField.upload_to - see model field reference.
    
    To conserve inodes and have fewer directories inside tansu (we
    hope we get enough files to have this problem!), add subdirectories
    composed of initial digits of file_object.id.
    
    >>> img = ImageObject
    >>> img.id = 1
    >>> get_item_files_path(img, 'img.jpg')
    'tansu/1/1/img.jpg'
    >>> img.id = 56
    >>> get_item_files_path(img, 'img.jpg')
    'tansu/5/56/img.jpg'
    >>> img.id = 2501
    >>> get_item_files_path(img, 'img.jpg')
    'tansu/2/2501/img.jpg'
    """
    entity_id = str(file_object.entity.id)
    if len(entity_id) == 1:
        subdirs = '%s/%s' % (entity_id, entity_id)
    else:
        subdirs = '%s/%s' % (entity_id[0], entity_id)
    return '%s%s/%s' % (MEDIA_PATH, subdirs, filename)


class Instance(models.Model):
    entity = models.ForeignKey(Entity)
    model = models.CharField(max_length=32)
    object_id = models.IntegerField()
    
    class Meta:
        unique_together = (('model', 'object_id'),)

class FileObject(BaseModel):
    entity = models.ForeignKey(Entity)
    is_master = models.BooleanField()
    description = models.TextField(blank=True)
    size = models.IntegerField()
    uri = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.media.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('tansu-detail', (), {'id': self.id })
    
    def save(self):
        if hasattr(self, 'media'):
            self.size = self.media.size
            self.uri = self.media.name
        super(FileObject, self).save()
        instance = self.instance()
    
    def instance(self):
        """Gets connection between Entity and various FileObject subclasses.
        """
        if (not hasattr(self, '_instance')) or self._instance:
            content_type = ContentType.objects.get_for_model(self)
            try:
                self._instance = Instance.objects.get(self.entity.id, 'imagefile', self.id)
            except:
                self._instance = Instance(entity=self.entity,
                                          model=content_type.model,
                                          object_id=self.id)
                self._instance.save()
        return self._instance
    
    def filename(self):
        return self.media.name.replace(MEDIA_PATH,'')


class AudioFile(FileObject):
    media = models.FileField(upload_to=get_object_upload_path)
    
    class Meta:
        verbose_name = 'Audio Recording'
        verbose_name_plural = 'Audio Recordings'
    
    def save(self):
        super(AudioFile, self).save()
    
    def edit_url(self):
        return '/admin/tansu/audiofile/%s/' % self.id
    
    def mimetype(self):
        return 'audio'


class DocumentFile(FileObject):
    media = models.FileField(upload_to=get_object_upload_path)
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    
    def save(self):
        super(DocumentFile, self).save()
    
    def edit_url(self):
        return '/admin/tansu/documentfile/%s/' % self.id
    
    def mimetype(self):
        return 'document'


class ImageFile(FileObject):
    media = models.ImageField(upload_to=get_object_upload_path)
    
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
    
    def save(self):
        """Uploads image to mediawiki, or updates description for existing file.
        """
        super(ImageFile, self).save()
        #if self.media:
        #    page_name = 'File:%s' % self.media.name.replace(IMAGEFILE_PATH,'')
        #    if not wiki.exists(page_name):
        #        path = '/'.join([settings.MEDIA_ROOT, self.media.name]).replace('//', '/')
        #        response = wiki.upload_file(path, self.description)
        #    else:
        #        response = wiki.update_file(page_name, self.description)
    
    def delete(self):
        """Deletes image from mediawiki.
        """
        super(ImageFile, self).delete()
        if self.media:
            page_name = 'File:%s' % self.media.name
            response = wiki.update_file(page_name, self.description)
            assert False
    
    def edit_url(self):
        return '/admin/tansu/imagefile/%s/' % self.id
    
    def mimetype(self):
        return 'image'


class VideoFile(FileObject):
    url = models.URLField()
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
    
    def save(self):
        super(VideoFile, self).save()
    
    def edit_url(self):
        return '/admin/tansu/videofile/%s/' % self.id
    
    def mimetype(self):
        return 'video'
