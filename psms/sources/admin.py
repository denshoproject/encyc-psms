from django.conf import settings
from django.contrib import admin

from sources.models import Source


class SourceAdmin(admin.ModelAdmin):
    fieldsets = (
            #'created',
            #'modified',
        (None, {'fields': (
            ('published','headword',),
            ('densho_id','encyclopedia_id',),
        )}),
        (None, {'fields': (
            ('media_format', 'aspect_ratio'),
            ('original', 'streaming_url', 'transcript'),
            ('display','update_display'),
        )}),
        (None, {'fields': (
            ('institution_id','collection_name',),
            'external_url',
        )}),
        (None, {'fields': (
            'caption', 'caption_extended',
            'courtesy',
        )}),
        (None, {'fields': (
            'creative_commons',
        )}),
        (None, {'fields': (
            'notes',
        )}),
    )
    list_display = (
        'published',
        'is_valid',
        'media_format',
        'densho_id',
        'encyclopedia_id',
        'headword',
        'caption',
        )
    list_display_links = ['densho_id',]
    ordering = ['headword', 'densho_id',]
    list_filter = ['published', 'media_format', 'aspect_ratio', 'creative_commons',]
    search_fields = [
        'headword',
        'densho_id', 'encyclopedia_id',
        'caption', 'caption_extended', 'courtesy',
        'institution_id', 'collection_name',
        'original', 'display', 'external_url',
        'media_format',
        'creative_commons',
        'notes',
        ]
    
    def render_change_form(self, request, context, *args, **kwargs):
        """If Source has been saved, insert link to MediaWiki article (using headword).
        """
        if context.get('original', None):
            txt = 'Title of wiki article this primary source is connected to. ' \
                  '<strong><a href="%s/%s">Back to article</a></strong>' % (settings.EDITORS_MEDIAWIKI_URL,
                                                                            context['original'].headword)
        else:
            txt = 'Title of wiki article this primary source is connected to.'
        context['adminform'].form.fields['headword'].help_text = txt
        return super(SourceAdmin, self).render_change_form(request, context, args, kwargs)

admin.site.register(Source, SourceAdmin)
