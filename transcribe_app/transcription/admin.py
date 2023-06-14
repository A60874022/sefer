from django.contrib import admin

from transcription.models import Transcription, TextBlock


# Register your models here.
@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "audio_url",
        "audio",
        "text",
    )


admin.site.register(TextBlock)
