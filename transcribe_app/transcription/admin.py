from django.contrib import admin

from .models import TextBlock, Transcription, City, Personalities


class TextBlockInline(admin.StackedInline):
    model = TextBlock


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    inlines = [TextBlockInline]


admin.site.register(City)
admin.site.register(Personalities)
