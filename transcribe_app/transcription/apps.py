from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TranscriptionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transcription"
    verbose_name = _("Транскрипция")
