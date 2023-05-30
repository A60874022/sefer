from django.db import models


class AudioFile(models.Model):
    """Класс загружаемого аудио файла."""
    pass


class Trancription(models.Model):
    """Класс транскрипции текста."""
    audio_url = models.URLField()
    audio = models.FileField(upload_to='/media')
    text = models.CharField()
    keywords = models.ManyToManyField('Keywords')
    personalities = models.ManyToManyField('Personalities')


class Keywords(models.Model):
    """Ключевые слова."""
    name = models.TextField('Keyword_name', max_length=60)

    def __str__(self):
        return self.name


class Personalities(models.Model):
    """Персоналии."""
    name = models.TextField('Personality_name')

    def __str__(self):
        return self.name
