from django.contrib import admin

from sources.models import Source


class SourceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            #'created',
            #'modified',
            'headword',
            'densho_id',
            'encyclopedia_id',
            'caption',
            'courtesy',
            'institution_id',
            'collection_name',
            'external_url',
            'creative_commons',
            'media_format',
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
        'densho_id',
        'encyclopedia_id',
        'headword',
        'caption',
        'courtesy',
        'institution_id',
        'collection_name',
        'external_url',
        'creative_commons',
        'media_format',
        'notes',
        ]

admin.site.register(Source, SourceAdmin)
