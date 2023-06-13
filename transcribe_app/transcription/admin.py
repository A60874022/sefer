from django.contrib import admin

from .models import Trancription, Keywords, Personalities


class KeywordsAdmin(admin.ModelAdmin):
    """Админка ключевых слов."""
    
    list_display = ('id', 'name')
    

class PersonalitiesAdmin(admin.ModelAdmin):
    """Админка персоналий."""
    
    list_display = ('id', 'name')


class TrancriptionAdmin(admin.ModelAdmin):
    """Админка текста транскрибации."""

    filter_horizontal = ('keywords', 'personalities')
    list_display = (
        'id',
        'text',
    )
    list_display_links = ('id', 'text')
    empty_value_display = '-пусто-'

admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Personalities, PersonalitiesAdmin)
admin.site.register(Trancription, TrancriptionAdmin)
