import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from transcription.models import City, Keywords, Personalities, TextBlock, Transcription


class KeywordsSerializer(serializers.ModelSerializer):
    """Сериализатор для городов."""

    class Meta:
        model = Keywords
        fields = ("name",)


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
    text_blocks = TextBlockSerializer(
        many=True
    )  # Вложенный сериализатор для text_blocks
    audio_url = serializers.URLField()

    class Meta:
        model = Transcription
        fields = ("id", "name", "audio", "audio_url", "text_blocks")

    def create(self, validated_data):
        """Создание текстовых блоков через пост запрос."""
        text_blocks_data = validated_data.pop("text_blocks")
        transcription = Transcription.objects.create(**validated_data)
        for text_block_data in text_blocks_data:
            TextBlock.objects.create(transcription=transcription, **text_block_data)
        return transcription

    def update(self, instance, validated_data):
        """
        Обновление записи в том числе  и текстовых блоков.
        ВАЖНО: при обновлении и правке данных необходимо скопировать все текстовые блоки
        в патч запрос и только после этого редактировать от отправлять, так как если
        будут переданы только старые данные то предыдущие будут утеряны.
        """
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.audio = validated_data.get("audio", instance.audio)
        instance.audio_url = validated_data.get("audio_url", instance.audio_url)

        if "text_blocks" in validated_data:
            text_blocks_data = validated_data.pop("text_blocks")
            instance.text_blocks.all().delete()  # Удаляем старые text_blocks
            for text_block_data in text_blocks_data:
                TextBlock.objects.create(transcription=instance, **text_block_data)

        instance.save()
        return instance
