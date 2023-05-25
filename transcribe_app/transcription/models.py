from django.db import models


class Trancription(models.Model):
    text = models.CharField()
    keywords = models.ManyToManyField('Keywords')
    personalities = models.ManyToManyField('Personalities')


class Keywords(models.Model):
    name = models.TextField(max_length=60)

    def __str__(self):
        return self.name


class Personalities(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name
