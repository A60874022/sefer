import os

from django.db import models
from django.dispatch import receiver


class Transcription(models.Model):
    """Класс транскрипции текста."""

    audio_url = models.URLField("Backet_url_name", blank=True, max_length=500)
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


class City(models.Model):
    """Модель, представляющая город."""

    name = models.CharField("Город", max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Personalities(models.Model):
    """Модель, представляющая персоналии."""

    name = models.CharField("Персоналия", max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Персоналия"
        verbose_name_plural = "Персоналии"


class Keywords(models.Model):
    """Модель, представляющая ключевые слова."""

    name = models.CharField("Ключевое слово", max_length=100, unique=True)
    parent = models.ForeignKey(
        "Keywords",
        on_delete=models.CASCADE,
        verbose_name="родитель",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"


class TextBlock(models.Model):
    """Модель текстовых блоков."""

    minute = models.PositiveIntegerField("Минута")
    text = models.TextField("Текст")
    transcription = models.ForeignKey(
        Transcription, on_delete=models.CASCADE, related_name="text_blocks"
    )
    keywords = models.ManyToManyField(
        Keywords, verbose_name="Ключевые слова", blank=True
    )

    personalities = models.ManyToManyField(
        Personalities, verbose_name="Персоналии", blank=True
    )
    cities = models.ManyToManyField(City, verbose_name="Города", blank=True)

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
        return (
            f"Название транскрипции: {self.transcription.name}. "
            f"Минута: {self.minute}"
        )
