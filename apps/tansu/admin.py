from django.contrib import admin

from tansu.models import ImageFile

class ImageFileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'image', 
            'title', 
            'description', 
#            'created', 
#            'modified', 
        )}),
    )
    list_display = ['image', 'title',]
    list_display_links = ['image']
#    ordering = ['-created']
    #list_filter = []
    search_fields = [
        'image', 
        'title', 
        'description', 
    ]

admin.site.register(ImageFile, ImageFileAdmin)
