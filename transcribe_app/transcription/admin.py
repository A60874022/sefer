from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import TextBlock, Transcription, City, Personalities, Keywords


class TextBlockInline(admin.StackedInline):
    model = TextBlock


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    inlines = [TextBlockInline]

class CityAdmin(ModelAdmin):
    list_display = ('name', 'is_admin')
    list_filter = ('name',)

class PersonalitiesAdmin(ModelAdmin):
    list_display = ('name', 'is_admin')
    list_filter = ('name',)

class KeywordsAdmin(ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

admin.site.register(City, CityAdmin)
admin.site.register(Personalities, PersonalitiesAdmin)
admin.site.register(Keywords, KeywordsAdmin)
