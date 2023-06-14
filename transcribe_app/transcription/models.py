from django.db import models


class Transcription(models.Model):
    """Класс транскрипции текста."""

    audio_url = models.URLField("backet_url_name", blank=True)
    audio = models.FileField("audio", upload_to="transcription/audio")
    text = models.TextField("transcription_text", blank=True)
    # keywords = models.ManyToManyField('Keywords')
    # personalities = models.ManyToManyField('Personalities')


# class Keywords(models.Model):
#     """Ключевые слова."""
#     name = models.TextField('Keyword_name', max_length=60)

#     def __str__(self):
#         return self.name


# class Personalities(models.Model):
#     """Персоналии."""
#     name = models.TextField('Personality_name')

#     def __str__(self):
#         return self.name


class TextBlock(models.Model):
    minute = models.PositiveIntegerField("Minute")
    text = models.TextField("Text")
    transcription = models.ForeignKey(
        Transcription,
        on_delete=models.CASCADE,
        related_name="textblock",
    )

    def __str__(self):
        return self.text
