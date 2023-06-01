from django.contrib import admin
from transcription.models import Trancription


# Register your models here.

@admin.register(Trancription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'audio_url',
        'audio',
        'text',
    )
