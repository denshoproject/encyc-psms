from django.contrib import admin

from sources.models import Source


class SourceAdmin(admin.ModelAdmin):
    fieldsets = (
            #'created',
            #'modified',
        (None, {'fields': (
            'headword',
            ('densho_id','encyclopedia_id',),
            ('institution_id','collection_name',),
        )}),
        (None, {'fields': (
            'caption',
            'courtesy',
        )}),
        (None, {'fields': (
            ('media','display',),
            'external_url',
            ('media_format','creative_commons',),
        )}),
        (None, {'fields': (
            'notes',
        )}),
    )
    list_display = [
        'densho_id',
        'encyclopedia_id',
        'headword',
        'caption',
        ]
    list_display_links = ['densho_id',]
    ordering = ['headword', 'densho_id',]
    list_filter = ['media_format','creative_commons','institution_id',]
    search_fields = [
        'headword',
        'densho_id', 'encyclopedia_id',
        'caption', 'courtesy',
        'institution_id', 'collection_name',
        'media', 'display', 'external_url',
        'media_format',
        'creative_commons',
        'notes',
        ]

admin.site.register(Source, SourceAdmin)
