from django.db import models


class Transcription(models.Model):
    """Класс транскрипции текста."""

    audio_url = models.URLField("Backet_url_name", blank=True)
    audio = models.FileField("Аудио", upload_to="transcription/audio")
    name = models.CharField("Название", max_length=60)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Транскрипция"
        verbose_name_plural = "Транскрипции"


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
        verbose_name = "text_block"
        verbose_name_plural = "text_blocks"
        constraints = [
            models.UniqueConstraint(
                fields=["minute", "text", "transcription"],
                name="uniq_transcriptions_text_block",
            )
        ]
