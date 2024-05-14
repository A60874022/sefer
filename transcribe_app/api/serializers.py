import base64

from django.core.files.base import ContentFile
from django.db.models import ManyToManyField
from rest_framework import serializers

from transcription.models import (City, Keywords, Personalities, TextBlock,
                                  Transcription, Country)


class KeywordsSerializer(serializers.ModelSerializer):
    """Сериализатор для ключевых слов."""

    class Meta:
        model = Keywords
        fields = ("id", "name",)


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для городов."""

    class Meta:
        model = City
        fields = ("id", "name", "country")


class CountrySerializer(serializers.ModelSerializer):
    """Сериализатор для Стран."""

    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ("id", "name", "cities")


class CountryGlossarySerializer(serializers.ModelSerializer):
    """Сериализатор для Стран в глоссарии."""

    class Meta:
        model = Country
        fields = ("id", "name")


class PersonalitiesSerializer(serializers.ModelSerializer):
    """Сериализатор для персоналий."""

    class Meta:
        model = Personalities
        fields = ("id", "name",)


class TextBlockSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока."""

    class Meta:
        model = TextBlock
        fields = (
            "id", "minute", "text",
            "keywords", "personalities", "cities", "countries"
        )


class TextBlockGetSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока."""
    keywords = serializers.StringRelatedField(many=True)
    personalities = serializers.StringRelatedField(many=True)
    cities = serializers.StringRelatedField(many=True)
    countries = serializers.StringRelatedField(many=True)

    class Meta:
        model = TextBlock
        fields = (
            "id", "minute", "text",
            "keywords", "personalities", "cities", "countries"
        )


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
        """
        Создание транскрипции с текстовыми блоками через пост запрос.
        Поля тегов добавляются отдельно после создания текстового блока.
        """
        data_text_blocks = validated_data.pop("text_blocks")
        transcription = Transcription.objects.create(**validated_data)
        for block_data in data_text_blocks:
            tag_fields = [field.name for field in TextBlock._meta.get_fields()
                          if isinstance(field, ManyToManyField)]
            tag_data = {field: block_data.pop(field)
                        for field in tag_fields if field in block_data}
            text_block = TextBlock.objects.create(transcription=transcription,
                                                  **block_data)
            for tag, data in tag_data.items():
                text_block.__getattribute__(tag).set(data)
        return transcription

    def update(self, instance, validated_data):
        """
        Обновление записи в том числе  и текстовых блоков.
        ВАЖНО: при обновлении и правке данных необходимо скопировать
        все текстовые блоки в патч запрос и только после этого редактировать,
        так как если будут переданы только старые данные то предыдущие
        будут утеряны.
        """
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.audio = validated_data.get("audio", instance.audio)
        instance.audio_url = validated_data.get("audio_url",
                                                instance.audio_url)

        if "text_blocks" in validated_data:
            data_text_blocks = validated_data.pop("text_blocks")
            instance.text_blocks.all().delete()  # Удаляем старые text_blocks
            for block_data in data_text_blocks:
                tag_fields = [
                    field.name for field in TextBlock._meta.get_fields()
                    if isinstance(field, ManyToManyField)
                ]
                tag_data = {field: block_data.pop(field)
                            for field in tag_fields if field in block_data}
                text_block = TextBlock.objects.create(transcription=instance,
                                                      **block_data)
                for tag, data in tag_data.items():
                    text_block.__getattribute__(tag).set(data)

        instance.save()
        return instance


class TranscriptionShortSerializer(serializers.ModelSerializer):
    """Сериализатор для простого списка аудио."""
    class Meta:
        model = Transcription
        fields = ("id", "name")
