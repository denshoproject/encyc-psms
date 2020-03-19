from django.contrib import admin

from tansu.models import Entity, AudioFile, DocumentFile, ImageFile, VideoFile


class EntityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            #'created',
            #'modified',
            'uid',
            'title',
            'description',
        )}),
    )
    list_display = ['uid', 'title',]
    list_display_links = ['uid']
    #ordering = ['-created']
    #list_filter = []
    search_fields = [
        'uid',
        'title',
        'description',
    ]

class AudioFileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            #'created',
            #'modified',
            'entity',
            'is_master',
            'media',
            'description',
            'size',
            'uri',
        )}),
    )
    list_display = ['entity', 'media', 'is_master',]
    list_display_links = ['media']
    #ordering = ['-created']
    #list_filter = []
    search_fields = [
        'media',
        'description',
    ]

class ImageFileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            #'created',
            #'modified',
            'entity',
            'is_master',
            'media',
            'description',
            'size',
            'uri',
        )}),
    )
    list_display = ['entity', 'media', 'is_master',]
    list_display_links = ['media']
    #ordering = ['-created']
    #list_filter = []
    search_fields = [
        'media',
        'description',
    ]

class DocumentFileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            #'created',
            #'modified',
            'entity',
            'is_master',
            'media',
            'description',
            'size',
            'uri',
        )}),
    )
    list_display = ['entity', 'media', 'is_master',]
    list_display_links = ['media']
    #ordering = ['-created']
    #list_filter = []
    search_fields = [
        'media',
        'description',
    ]

class VideoFileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            #'created',
            #'modified',
            'entity',
            'is_master',
            'url',
            'description',
            'size',
            'uri',
        )}),
    )
    list_display = ['entity', 'url', 'is_master',]
    list_display_links = ['url']
    #ordering = ['-created']
    #list_filter = []
    search_fields = [
        'url',
        'description',
    ]

#admin.site.register(Entity, EntityAdmin)
#admin.site.register(AudioFile, AudioFileAdmin)
#admin.site.register(ImageFile, ImageFileAdmin)
#admin.site.register(DocumentFile, DocumentFileAdmin)
#admin.site.register(VideoFile, VideoFileAdmin)
