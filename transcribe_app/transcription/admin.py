from django.contrib import admin

from transcription.models import TextBlock, Transcription


# Register your models here.
@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "audio_url",
        "audio",
    )


admin.site.register(TextBlock)
