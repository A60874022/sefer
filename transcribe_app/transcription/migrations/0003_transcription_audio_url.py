# Generated by Django 4.2.1 on 2024-06-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transcription", "0002_alter_transcription_audio"),
    ]

    operations = [
        migrations.AddField(
            model_name="transcription",
            name="audio_url",
            field=models.URLField(
                blank=True, max_length=500, verbose_name="Backet_url_name"
            ),
        ),
    ]
