from django.db import models


class Trancription(models.Model):
    """Класс транскрипции текста."""
    text = models.TextField()
    keywords = models.ManyToManyField('Keywords')
    personalities = models.ManyToManyField('Personalities')


class Keywords(models.Model):
    """Ключевые слова."""
    name = models.TextField(max_length=60)

    def __str__(self):
        return self.name


class Personalities(models.Model):
    """Персоналии."""
    name = models.TextField()

    def __str__(self):
        return self.name
