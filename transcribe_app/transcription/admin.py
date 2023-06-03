from django.contrib import admin

from transcription.models import Transcription

# Register your models here.

@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'audio_url',
        'audio',
        'text',
    )
