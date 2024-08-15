from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from transcription.models import (City, Country, Keywords, Personalities,
                                  TextBlock, Transcription)
from transcription.services import create_transcription, delete_file_in_backet


class KeywordsSerializer(serializers.ModelSerializer):
    """Сериализатор для ключевых слов."""

    class Meta:
        model = Keywords
        fields = (
            "id",
            "name",
        )


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для городов."""

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "country",
        )


class CountrySerializer(serializers.ModelSerializer):
    """Сериализатор для Стран."""

    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "cities",
        )


class CountryGlossarySerializer(serializers.ModelSerializer):
    """Сериализатор для Стран в глоссарии."""

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "creator",
        )


class PersonalitiesSerializer(serializers.ModelSerializer):
    """Сериализатор для персоналий."""

    class Meta:
        model = Personalities
        fields = (
            "id",
            "name",
        )


class TextBlockSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока."""

    class Meta:
        model = TextBlock
        fields = (
            "id",
            "time_start",
            "time_end",
            "text",
            "transcription",
            "keywords",
            "personalities",
            "cities",
            "countries",
        )


class TextBlockGetSerializer(serializers.ModelSerializer):
    """Сериализатор текстового блока при сохранении файла и ручной расшифровкой."""

    class Meta:
        model = TextBlock
        fields = (
            "id",
            "time_start",
            "time_end",
            "text",
        )


class TranscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки аудио для автоматической расшифровки."""

    class Meta:
        model = Transcription
        fields = (
            "id",
            "name",
            "audio",
            "transcription_status",
        )

    @transaction.atomic
    def create(self, validated_data):
        """
        Создание транскрипции с текстовыми блоками через пост запрос.
        Поля тегов добавляются отдельно после создания текстового блока.
        """
        transcription_date = timezone.now()
        transcription = Transcription.objects.create(
            **validated_data, transcription_date=transcription_date
        )
        last = Transcription.objects.filter(pk__gt=1).last()
        text = create_transcription(last.id)
        print(text)
        TextBlock.objects.bulk_create(
            [
                TextBlock(
                    time_start=minute, time_end=minute + 1, text=" ".join(chunk), transcription=transcription
                )
                for minute, chunk in enumerate(text, start=1)
            ]
        )
        transcription.save()
        delete_file_in_backet(last.id)
        return transcription


class TranscriptionPartialSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки частичной автоматической расшифровки аудио."""

    class Meta:
        model = Transcription
        fields = (
            "id",
            "name",
            "audio",
            "transcription_status",
        )


class TranscriptionGetSerializer(serializers.ModelSerializer):
    """Сериализатор для get запроса при автоматической полной расшифровки аудио."""

    class Meta:
        model = Transcription
        fields = (
            "id",
            "name",
            "audio",
            "transcription_status",
            "creator",
            "last_updated",
        )
