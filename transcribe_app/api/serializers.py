import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from transcription.models import TextBlock, Transcription


class TextBlockSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока."""

    class Meta:
        model = TextBlock
        fields = ("minute", "text")


class Base64AudioField(serializers.FileField):
    """Функция для декодирования аудио файла из формата base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:audio"):
            format, audio_str = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(audio_str), name="temp." + ext)

        return super().to_internal_value(data)


class TranscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки аудио."""

    audio = Base64AudioField()
    textblocks = serializers.SerializerMethodField(read_only=True)

    def get_textblocks(self, obj):
        queryset = obj.textblocks.all()
        serializer = TextBlockSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Transcription
        fields = ("audio", "audio_url", "textblocks")
