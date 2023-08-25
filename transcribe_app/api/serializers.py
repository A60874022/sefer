import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from transcription.models import TextBlock, Transcription, Personalities, City
from rest_framework.serializers import SerializerMethodField

class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для городов."""

    class Meta:
        model = City
        fields = ("name",)


class PersonalitiesSerializer(serializers.ModelSerializer):
    """Сериализатор для персоналий."""

    class Meta:
        model = Personalities
        fields = ("name",)



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
    text_blocks = serializers.SerializerMethodField(read_only=True)
    audio_url = serializers.URLField(read_only=True)

    def get_text_blocks(self, obj):
        queryset = TextBlock.objects.filter(transcription__id=obj.id)
        serializer = TextBlockSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Transcription
        fields = ("id", "name", "audio", "audio_url", "text_blocks")
