import os
from django.db import models
from django.dispatch import receiver


class Transcription(models.Model):
    """Класс транскрипции текста."""

    audio_url = models.URLField("Backet_url_name", blank=True)
    audio = models.FileField("Аудио", upload_to="transcription/audio")
    name = models.CharField("Название", max_length=60)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Транскрипция"
        verbose_name_plural = "Транскрипции"


@receiver(models.signals.post_delete, sender=Transcription)
def auto_delete_media_file(sender, instance, *args, **kwargs):
    if instance.audio:
        if os.path.isfile(instance.audio.path):
            os.remove(instance.audio.path)


class TextBlock(models.Model):
    """Модель текстовых блоков."""

    minute = models.PositiveIntegerField("Минута")
    text = models.TextField("Текст")
    transcription = models.ForeignKey(
        Transcription,
        on_delete=models.CASCADE,
        related_name="text_blocks",
    )
    keywords = models.TextField("Ключевые слова.", blank=True, null=True)
    personalities = models.TextField("Персоналии", blank=True, null=True)

    class Meta:
        verbose_name = "Текстовый_блок"
        verbose_name_plural = "Текстовые_блоки"
        constraints = [
            models.UniqueConstraint(
                fields=["minute", "text", "transcription"],
                name="uniq_transcriptions_text_block",
            )
        ]

    def __str__(self) -> str:
        return f"Название транскрипции: {self.transcription.name}.\
                 Минута: {self.minute}"
