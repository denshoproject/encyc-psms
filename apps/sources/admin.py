from django.conf import settings
from django.contrib import admin

from sources.models import Source


class SourceAdmin(admin.ModelAdmin):
    fieldsets = (
            #'created',
            #'modified',
        (None, {'fields': (
            'headword',
            ('densho_id','encyclopedia_id',),
        )}),
        (None, {'fields': (
            'media_format',
            ('original', 'streaming_url', 'transcript'),
            ('display','update_display'),
        )}),
        (None, {'fields': (
            ('institution_id','collection_name',),
            'external_url',
        )}),
        (None, {'fields': (
            'caption',
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
        'is_valid',
        'densho_id',
        'encyclopedia_id',
        'headword',
        'caption',
        )
    list_display_links = ['densho_id',]
    ordering = ['headword', 'densho_id',]
    list_filter = ['media_format','headword',]
    search_fields = [
        'headword',
        'densho_id', 'encyclopedia_id',
        'caption', 'courtesy',
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
